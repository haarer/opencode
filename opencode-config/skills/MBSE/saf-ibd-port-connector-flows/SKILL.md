---
name: saf-ibd-port-connector-flows
description: Build SAF IBD (internal block diagram / composite structure) structures — typed proxy ports on part types, the realizing connector, and InformationFlow/ItemFlow item exchanges draped over it — across the Operational (O*), Conceptual (C*), and Physical (P*) domains. Use when modeling SAF context-exchange IBD viewpoints (O1_OCXE, C1_SCXE, P1_PCXE), creating parts, ports, connectors, exchange types, item flows, or linking item flows to a connector in a SAF model.
---

# SAF IBD: ports, connectors, item flows

## Model shape (memorize before touching anything)

- Parts live on the WHOLE Block (`create_part`, typed by the part-type Block).
- Ports live on the part's TYPE (the classifier), never on the part property.
- The Connector lives on the whole Block, wiring partProperty -> port on that part's type.
- Item Flows live in the context PACKAGE (owned by neither block) and are draped over the connector via the realizing-connector reference.
- Exchange types are a viewpoint in their own right — each domain defines them via its Exchange Type Definition viewpoint, each realized in its own exchange-types package and documented by its own BDD/table view.

## Domain matrix (memorize — match the IBD's domain everywhere)

Every domain has its own context-exchange IBD and its own exchange types living in that domain's ETD viewpoint. The IBD domain, its parts/kinds, and its exchange types must all agree.

| Domain | Context-exchange IBD | Exchange types live in | Exchange-type stereotype | ETD view stereo |
|---|---|---|---|---|
| Operational (O) | O1_OCXE | O2_OETD | SAF_OperationalExchangeType | SAF_O2_OETD |
| Conceptual (C) | C1_SCXE | C2_SETD | SAF_ConceptualExchangeType | SAF_C2_SETD |
| Physical (P) | P1_PCXE | P2_PETD | SAF_PhysicalExchangeType | SAF_P2_PETD |

A P1_PCXE IBD uses SAF_PhysicalExchangeType types from P2_PETD; a C1_SCXE IBD uses SAF_ConceptualExchangeType types from C2_SETD; an O1_OCXE IBD uses SAF_OperationalExchangeType types from O2_OETD. Never mix domains.

## Quick start checklists

1. Parts
   - Part-type blocks must exist (SAF kinds: operational_performer, conceptual_system, physical_system, ...).
   - `create_part(wholeBlockId=<context block>, partTypeBlockId=<participant>, name=<role>_<n>, multiplicity)`. Add a SAF role stereotype only if the viewpoint needs it.
   - Do NOT also call `create_relationship(type='composition')` for the same whole/part pair — `create_part` auto-creates the companion Association.

2. Ports on the part TYPE
   - Create an InterfaceDefinition block once (e.g. "OpenVPN Interface"); it types the ports.
   - On each part-type block: create a Port (`type='Port'`), apply `<<ProxyPort>>`, then `set_type(portId, interfaceId)`.
   - Symmetric ports for each side that participates in the exchange.

3. Connector on the whole
   - `create_connector(wholeBlockId=<context block>, end1PartId=<part property>, end1PortId=<port on that part's type>, end2PartId=..., end2PortId=...)`. Name it by its endpoints ("client to server connection").

4. Exchange types (their own viewpoint)
   - Look up the IBD's domain in the matrix above; the exchange types live in that domain's ETD viewpoint (O2_OETD / C2_SETD / P2_PETD), in a package named for it (e.g. "P2_PETD - Physical Exchange Types").
   - In that package: create Classifiers (Class or DataType) per exchanged item kind and apply that domain's exchange-type stereotype from the matrix.
   - Their types/relationships are documented by the ETD view (BDD or table, the ETD view stereo from the matrix), and they carry traceability to the next-upper domain's exchange types (realizing/typing: physical -> conceptual -> operational).

5. Item flows — link them to the modeler's chosen realizing element
   - ITEM FLOWS CONNECT TO THE PORTS, NOT THE PARTS: `create_information_flow(sourceId=<proxy port on source part's type>, targetId=<proxy port on target part's type>, conveyedItemId=<exchange-type classifier>, name="flow for <X> (<direction>)", realizingConnectorId=<connector>)`.
   - IF THE FLOW IS REALIZED BY A CONNECTOR, ITS ENDS MUST MATCH THE CONNECTOR'S ENDS: the flow's source port and target port must be exactly the connector's two end roles (same part-with-port pairing, port-to-port). A flow whose ends are the whole-block part properties (instead of the ports) does not pair with the connector and is WRONG.
   - Conveyed must be an exchange type of the IBD's OWN domain (from that domain's ETD viewpoint); direction must match the observed exchange (capture/pcap), one flow per direction.
   - The connector must exist before creating its flows; if `create_information_flow` reports the connector not found, the connector was removed/renumbered — look it up fresh (block structure / find) and link afterward with the setter.
   - The conveyed classifier must be an exchange type of the IBD's OWN domain (from that domain's ETD viewpoint).
   - CONNECTOR CHOICE IS A MODELER DECISION. The realizing connector is the connection the flow drapes over. Decide as follows:
     - One connector: no choice — link to it.
     - Multiple connectors: the connectors (and their port ends) carry intent — the LLM usually created them and can derive which flow belongs on which connection from the connector/port/interface names and the flow's content and direction. Match the proper one.
     - Only ask the user when the intent genuinely cannot be derived; do not silently pick an arbitrary one.
   - Existing flows: `set_information_flow_realizing(flowId, realizingConnectorId?, realizingActivityEdgeId?, realizingMessageId?)` (clears-then-sets per kind). The connector-only `set_information_flow_realizing_connector(flowId, connectorId)` is a backward-compat wrapper.
   - Every flow must report `realizingConnectors: 1`. The reference is bidirectional (InformationFlow::realizingConnector <-> Connector::informationFlowOfRealizingConnector); one connector may realize many flows.
   - REALIZATION IS NOT LIMITED TO CONNECTORS: an item flow can instead be realized by an activity object flow (`realizingActivityEdge`) or a sequence message (`realizingMessage`). That is how behavior viewpoints (activity/sequence) get linked to the flow/interface-based viewpoints. FFDS does this; a connector-only IBD (like the OpenVPN P1_PCXE build) does not. The MCP surface supports all three kinds: create_information_flow accepts realizingConnectorId / realizingActivityEdgeId / realizingMessageId, and set_information_flow_realizing replaces per kind (set_information_flow_realizing_connector kept as a backward-compat wrapper).

6. Diagram
   - `saf_create_diagram(diagramType='Composite Structure Diagram', elementIds=[the part properties], parentId=<context package>)` — a focused IBD showing parts and the connector. Verify the diagram carries the SAF_<VP> view stereotype (e.g. `SAF_P1_PCXE`), not a bare IBD.

## Verify a build

- Every flow: source/target = the connector's ports (port-to-port, ends matching the connector's end roles), realizing reference points at the modeler's chosen element (the intended connector / object flow / message), conveyed = the exchange type, name matches content+direction.
- Diagram detection: `saf_get_viewpoint_views` can return 0 for PV while `cameo://saf-views` finds the view — trust `cameo://saf-views` (stereotype-driven, not hardcoded).

## See REFERENCE.md for field-by-field tool contracts and a worked example.