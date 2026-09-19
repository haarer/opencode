# REFERENCE — SAF IBD tool contracts

Detailed contracts for the tools used by this skill. IDs in examples are illustrative.

## Parts

### create_part
`cameo_create_part(wholeBlockId, name, partTypeBlockId, multiplicity='1', aggregation='none', roleStereotype=optional)`

- Creates a typed part Property owned by the whole Block (internal structure). Property is `<<PartProperty>>`; `roleStereotype` (e.g. SAF_PhysicalInternalRole) applied on top if the viewpoint calls for it.
- `aggregation='composite'|'shared'` makes MagicDraw auto-create the companion Association (the composition line on a BDD) — that is expected. Never add a separate composition for the same pair.

Example:
```json
{ "wholeBlockId": "_2026x_1_26f0132_1789802087799_214746_4306", "name": "clientPC",
  "partTypeBlockId": "_2026x_1_26f0132_1789802091297_407152_4307" }
```

Multiplicity tweaks after creation: `cameo_set_multiplicity(elementId, '0..1')`.

## Ports

### create_element(type='Port') + ProxyPort + set_type
1. Create the InterfaceDefinition block that types the ports (one per interface, e.g. "OpenVPN Interface").
2. On EACH part-type block create a Port: `cameo_create_element(type='Port', name='openvpn client if', parentId=<part-type block>)`.
3. Apply `<<ProxyPort>>`: `cameo_apply_stereotype(elementId=port, stereotype='SAF_ProxyPort')`.
4. `cameo_set_type(elementId=port, typeId=<interface block>)`.

The port must be owned by the part's TYPE (classifier), the connector end then references it from the part property.

## Connector

### create_connector
`cameo_create_connector(wholeBlockId, end1PartId, end1PortId, end2PartId, end2PortId, end1Multiplicity='1', end2Multiplicity='1', name=optional)`

- Ends: endNPartId = a part property owned by the whole; endNPortId = a port owned by endNPart's type. Validated: part's type must own the port, part must be owned by the whole.
- Added to the whole's ownedConnectors → renders between the parts in the IBD.

Example (context block owns parts clientPC / vpnServer; ports on Client PC / VPN Server types):
```json
{ "wholeBlockId": "<context block>",
  "end1PartId": "<clientPC part>", "end1PortId": "<openvpn client if port>",
  "end2PartId": "<vpnServer part>", "end2PortId": "<openvpn server if port>" }
```

## Exchange types (their own viewpoint)

Exchange types are modeled inside the domain's Exchange Type Definition (ETD) viewpoint — not as ad-hoc helpers of the IBD. The context-exchange IBD, the parts/kinds, and the exchange types must all come from the SAME domain:

| Domain | Context-exchange IBD (IBD stereo) | Exchange-type VP | Exchange-type stereo | ETD view stereo |
|---|---|---|---|---|
| Operational | O1_OCXE (SAF_O1_OCXE) | O2_OETD | SAF_OperationalExchangeType | SAF_O2_OETD |
| Conceptual / System | C1_SCXE (SAF_C1_SCXE) | C2_SETD | SAF_ConceptualExchangeType | SAF_C2_SETD |
| Physical | P1_PCXE (SAF_P1_PCXE) | P2_PETD | SAF_PhysicalExchangeType | SAF_P2_PETD |

Cross-domain: physical types realize the conceptual types they implement; conceptual types refine operational ones. The ETD viewpoints exist to capture that traceability ("From which conceptual item is a physical item derived?").

- Create the classifier in a package named for the ETD viewpoint (e.g. "P2_PETD - Physical Exchange Types").
- Element: classifier kind Class or DataType (`cameo_create_element(type='DataType'|'Class')`) + `cameo_apply_stereotype(..., 'SAF_PhysicalExchangeType')` (domain-appropriate).
- The ETD viewpoint's presentation is a BDD featuring the exchange types, their properties, relationships, and cross-domain traceability ("From which conceptual item is a physical item derived?" — realizing/typing associations to the upper layer).
- Optionally create the ETD view itself: `saf_create_diagram(diagramType='Class Diagram', elementIds=[the exchange-type classifiers], parentId=<ETD package>)`, then verify stereo `SAF_P2_PETD` (or table variant).

### create_element(type='DataType') + SAF stereotype
- Parent: the exchange-types package of the viewpoint (P2_PETD, C2_CETD, O2_OETD...).
- `cameo_create_element(type='DataType', name='TLS Handshake Message', parentId=<packages>)` then `cameo_apply_stereotype(elementId=..., stereotype='SAF_PhysicalExchangeType')` (use the domain-appropriate one).

## Item flows

### create_information_flow
`cameo_create_information_flow(parentId, name, sourceId, targetId, conveyedItemId, realizingConnectorId, documentation=optional)`

- Lives in the context package. Source/target = the PROXY PORTS (`ProxyPort`s typed by the interface) on the two part types — NOT the part properties. When the flow is realized by a connector, its ends must match the connector's ends exactly (same ports, same part-with-port pairing, port-to-port); that is what lets the item flow drape over the connector on the IBD.
- Conveyed = the exchange-type classifier (applies ItemFlow + realizes the flow).
- `realizingConnectorId` optional at creation; when passed, the connector end registrations happen in one step. If it errors "not found", the connector was removed/renumbered — re-resolve and call the setter instead.
- Name convention: `flow for <ExchangeType> (<direction>)`, e.g. `flow for TLS Handshake Message (client to server)`.

### set_information_flow_realizing_connector
`cameo_set_information_flow_realizing_connector(flowId, connectorId)` — for flows created without the link (or to re-point). Clears any existing realizing connectors, sets the one, and reflects the reverse reference on the Connector. Returns `{ ..., realizingConnectors: 1, updated: true }`. Backward-compat convenience wrapper around `set_information_flow_realizing`.

### set_information_flow_realizing
`cameo_set_information_flow_realizing(flowId, realizingConnectorId?, realizingActivityEdgeId?, realizingMessageId?)` — the generalized setter. Each provided reference replaces THAT kind's realizing list (clear-then-add) and leaves the other kinds untouched (a flow may be realized by a connector AND a message in two diagrams). Each id is metaclass-validated (`Connector` / `ActivityEdge` via `mdbasicactivities` / `Message` via `mdbasicinteractions`). At least one realizing* arg required. Returns `{ ..., realizingConnectors, realizingActivityEdges, realizingMessages }` plus per-kind id/name.

Missing link symptom: the item flow exists but does not drape over the connector on the IBD. Fix by running this setter — do NOT recreate the flow.

### Realizing references — connector choice is a modeler decision
`InformationFlow` carries THREE realizing reference lists (UML properties, all exposed by MagicDraw):

| Reference | UML property | Realizes linkage to |
|---|---|---|
| Connector | `realizingConnector` | IBD connectors (what this skill's MCP tools set today) |
| ActivityEdge | `realizingActivityEdge` | object flows on activity diagrams |
| Message | `realizingMessage` | messages on sequence diagrams |

- Which connector (or object flow / message) realizes a flow is a MODELER DECISION. Resolve it like this:
     1. One connector -> no choice, set it.
     2. Multiple connectors -> the connectors and their port ends carry intent; derive which flow belongs on which connection from the connector name, its port roles/interfaces, and the flow's content and direction. The LLM usually created the connectors itself, so it knows the intent behind each. Choose the proper match.
     3. Only ask the user if the intent cannot be derived — never silently pick an arbitrary connector.
   - A single connector may realize many flows; a flow realizes over exactly the element chosen.
- Realizing by object flow or message is the mechanism that links BEHAVIOR viewpoints (activity, sequence) to the FLOW/INTERFACE viewpoints (item flows exchanged on interfaces). The FFDS reference model does this; connector-only builds (e.g. the OpenVPN P1_PCXE) do not.
- MCP surface status: ALL THREE kinds are surfaced. `create_information_flow` accepts `realizingConnectorId` / `realizingActivityEdgeId` / `realizingMessageId` at creation. `set_information_flow_realizing(flowId, realizingConnectorId?, realizingActivityEdgeId?, realizingMessageId?)` replaces per-kind lists (clear+add), leaves other kinds untouched, validates the resolved element's metaclass, and returns per-kind counts. `set_information_flow_realizing_connector(flowId, connectorId)` is kept as a backward-compat convenience wrapper.

## Diagram

### saf_create_diagram
`cameo_saf_create_diagram(name, parentId, diagramType='Composite Structure Diagram', elementIds=[...])`

- Pass elementIds = exactly the part properties you want visible (focused IBD, not everything owned).
- Connector shape comes from the whole's ownedConnectors (includeConnectors), or appears because the IBD shows the composite structure — call with the part ids and confirm.
- The diagram gets the SAF view stereotype (`SAF_P1_PCXE`) so `cameo://saf-views` reports it.

## Verification

- Flow link: reread via `set_information_flow_realizing_connector` return, or the flow's element fact sheet (`cameo://element/{id}`) — look for realizing connector on the InformationFlow and `informationFlowOfRealizingConnector` on the Connector.
- View detection: `cameo://saf-views` resource (runtime SAF-spec mapping). `saf_get_viewpoint_views` may under-report for PV domains.

## Worked example (OpenVPN P1_PCXE build)

The P-domain instance of the generic recipe. Substitute the O/C rows of the table above for an O1_OCXE or C1_SCXE build — the steps are identical otherwise.

1. Part types: `Client PC` (SoI), `VPN Server` blocks.
2. Parts on context block `OpenVPN System Context`: `clientPC`, `vpnServer`.
3. Interface block `OpenVPN Interface`; ProxyPorts `openvpn client if` (on Client PC) and `openvpn server if` (on VPN Server), both typed by the interface.
4. Connector `client to server connection` on the context block.
5. Exchange-types package `P2_PETD - Physical Exchange Types` with 5 `SAF_PhysicalExchangeType` DataTypes: OpenVPN Control Message, TLS Handshake Message, TLS ChangeCipherSpec Message, TLS Application Data Record, TLS Alert Message.
6. 7 item flows (directional, e.g. two Control Message flows C->S and S->C), each with `sourceId`/`targetId` = the matching `openvpn client if` / `openvpn server if` proxy ports (port-to-port, matching the connector's end roles), `conveyedItemId` = the DataType, `realizingConnectorId` = the connector.
7. IBD `OpenVPN System Context (P1_PCXE)` (Composite Structure Diagram) showing both parts; `SAF_P1_PCXE` applied; verified via `cameo://saf-views`.