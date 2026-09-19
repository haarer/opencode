# Reverse Engineering Code to UML Skill

## Overview

This skill guides an LLM through the process of reverse engineering source code into UML diagrams and documentation. It provides a structured workflow for analyzing code, identifying key components, creating appropriate UML diagrams, and capturing architectural learnings.

## Use Cases

- **Codebase Documentation**: Document existing codebases that lack UML documentation
- **Architecture Analysis**: Understand and visualize system architecture from source code
- **Legacy System Analysis**: Reverse engineer undocumented legacy systems
- **Code Review Preparation**: Create visual documentation before code review
- **Knowledge Transfer**: Document complex codebases for team onboarding
- **Migration Planning**: Understand code structure before refactoring or migration

## Workflow

### Phase 1: Codebase Analysis

**Goal**: Understand the overall structure and identify key components

**Steps:**
1. **Inventory Files and Packages**
   - List all source files
   - Identify package structure
   - Note file sizes and complexity indicators
   - Identify test files vs production code

2. **Identify Key Components**
   - Find entry points (main methods, application classes)
   - Identify core domain classes
   - Find interfaces and abstract classes
   - Note external dependencies (imports, packages)

3. **Understand Dependencies**
   - Map import relationships
   - Identify circular dependencies
   - Note external library dependencies
   - Find coupling between modules

**Output:**
- File structure diagram
- Package hierarchy
- Dependency map (high-level)

**Documentation Capture:**
```markdown
## Codebase Overview
- Total files: X
- Total lines of code: Y
- Languages: [List]
- Frameworks: [List]
- Entry points: [List]

## Key Observations
- [Observation 1]
- [Observation 2]
```

### Phase 2: Class Analysis

**Goal**: Understand individual classes and their responsibilities

**Steps:**
1. **Analyze Each Class**
   - Read class definition and documentation
   - Identify fields/properties
   - Identify methods/operations
   - Note visibility (public/private/protected)
   - Identify constructors

2. **Determine Responsibilities**
   - Use SOLID principles to understand class purpose
   - Identify single responsibilities
   - Note violations of SOLID
   - Classify as: Entity, Service, Repository, DTO, etc.

3. **Identify Relationships**
   - Composition (whole-part)
   - Aggregation (weak whole-part)
   - Association (bidirectional)
   - Dependency (uses)
   - Inheritance (generalization)

**Output:**
- Class diagram with key classes
- Class responsibility matrix (CRC)
- Relationship definitions

**Documentation Capture:**
```markdown
## Class: ClassName
### Responsibility
[Primary responsibility]

### Attributes
- `fieldName`: Type, Visibility, Purpose

### Operations
- `methodName()`: Purpose, Parameters, Return type

### Relationships
- **Composes**: OtherClass
- **Aggregates**: OtherClass
- **Uses**: OtherClass
- **Inherits**: ParentClass
```

### Phase 3: Behavior Analysis

**Goal**: Understand system behavior and interactions

**Steps:**
1. **Identify Use Cases/Features**
   - Find user-facing functionality
   - Identify business rules
   - Note external interactions (APIs, databases)

2. **Map Behaviors**
   - Identify state changes
   - Trace method calls
   - Map event handlers
   - Note async operations

3. **Create Sequence Diagrams**
   - For key workflows
   - For error handling paths
   - For external API interactions

**Output:**
- Use case list
- Key sequence diagrams
- State transition diagrams (if applicable)

**Documentation Capture:**
```markdown
## Key Workflows

### Workflow: [Name]
1. Trigger
2. Steps
3. Return values
4. Error conditions

## Business Rules
- [Rule 1]
- [Rule 2]
```

### Phase 4: Architecture Synthesis

**Goal**: Create comprehensive architecture documentation

**Steps:**
1. **Create Package Diagram**
   - Logical packages
   - Physical packages
   - Layer separation

2. **Create Component Diagram**
   - Major components
   - Dependencies
   - Interfaces

3. **Create Deployment Diagram**
   - Deployment targets
   - Physical nodes
   - Network topology

**Output:**
- Complete set of UML diagrams
- Architecture documentation

**Documentation Capture:**
```markdown
## Architecture Overview
- Layers: [List]
- Packages: [List]
- Components: [List]

## Design Patterns Identified
- [Pattern 1] in [Location]
- [Pattern 2] in [Location]

## Anti-Patterns Detected
- [Anti-pattern 1] in [Location]
- [Anti-pattern 2] in [Location]
```

### Phase 5: Learnings and Recommendations

**Goal**: Capture insights and improvement suggestions

**Steps:**
1. **Identify Strengths**
   - Good practices followed
   - Clean architecture elements
   - Well-designed components

2. **Identify Issues**
   - Code smells
   - Violations of principles
   - Technical debt

3. **Make Recommendations**
   - Refactoring suggestions
   - Documentation improvements
   - Architecture improvements

**Output:**
- Architecture review
- Refactoring backlog
- Quality metrics

**Documentation Capture:**
```markdown
## Strengths
- [Strength 1]
- [Strength 2]

## Issues
- [Issue 1]: Description, Impact, Severity
- [Issue 2]: Description, Impact, Severity

## Recommendations
- [Recommendation 1]: Priority, Effort
- [Recommendation 2]: Priority, Effort

## Next Steps
1. [Action 1]
2. [Action 2]
```

## Best Practices

### When Analyzing Code

1. **Start High-Level**
   - Understand the big picture first
   - Don't dive into details too early
   - Create overview diagrams before details

2. **Focus on What Matters**
   - Identify key components, not every class
   - Focus on business logic, not boilerplate
   - Prioritize by business importance

3. **Use Domain Language**
   - Translate technical terms to business terms
   - Use consistent terminology
   - Create a glossary

4. **Validate with Code**
   - Cross-reference diagrams with actual code
   - Update diagrams as you learn more
   - Keep documentation synchronized

5. **Capture Learnings**
   - Document assumptions
   - Note uncertainties
   - Record questions for clarification

### UML Diagram Selection

| Scenario | Recommended Diagrams |
|----------|---------------------|
| System overview | Package, Component |
| Class relationships | Class |
| Method interactions | Sequence, Communication |
| State changes | State Machine |
| Data flow | Activity, Use Case |
| Deployment | Deployment |
| Interface contracts | Interface |

### Documentation Quality

1. **Be Specific**
   - Avoid vague descriptions
   - Include file names and line numbers
   - Link to actual code when possible

2. **Be Consistent**
   - Use consistent terminology
   - Follow UML notation standards
   - Use templates for repeatable sections

3. **Be Actionable**
   - Make recommendations clear
   - Include effort estimates
   - Prioritize findings

## Example Templates

### Template: Class Documentation

```markdown
## Class: [ClassName]

**Location**: `[File]:[Line]`

### Responsibility
[Single sentence describing primary responsibility]

### Attributes
| Name | Type | Visibility | Purpose |
|------|------|------------|---------|
| field | Type | + | Description |

### Operations
| Method | Parameters | Return | Description |
|--------|------------|--------|-------------|
| method() | param1: Type | Type | Description |

### Relationships
- **Composes**: OtherClass (Multiplicity)
- **Aggregates**: OtherClass (Multiplicity)
- **Uses**: OtherClass (Multiplicity)
- **Inherits**: ParentClass

### Design Notes
[Design decisions, tradeoffs, constraints]

### TODO
- [ ] Questions to resolve
- [ ] Dependencies to clarify
```

### Template: Architecture Decision

```markdown
## Decision: [Title]

**Date**: YYYY-MM-DD

**Context**: 
[Why this decision was made, what problem it solves]

**Decision**:
[What was decided]

**Consequences**:
- Positive: [...]
- Negative: [...]
- Neutral: [...]

**Alternatives Considered**:
- [Alternative 1] - Why rejected
- [Alternative 2] - Why rejected

**References**:
- [Link to code]
- [Link to documentation]
```

### Template: Refactoring Recommendation

```markdown
## Recommendation: [Title]

**Priority**: High/Medium/Low
**Effort**: S/M/L
**Risk**: Low/Medium/High

**Current State**:
[Description of current code/structure]

**Problem**:
[What's wrong, why it needs fixing]

**Proposed Solution**:
[How to fix it]

**Benefits**:
- [Benefit 1]
- [Benefit 2]

**Implementation Steps**:
1. Step 1
2. Step 2
3. Step 3

**Testing Strategy**:
[How to verify the fix]

**Rollback Plan**:
[What to do if something breaks]
```

## Using the Cameo MCP Server

**Important**: When creating UML diagrams and elements in Cameo, use the **Cameo MCP Server** tools to interact with your model programmatically.

### MCP Server Tools

The Cameo MCP Server provides the following key tools:

- `create_element` - Create UML elements (Classes, Packages, Operations, etc.)
- `create_relationship` - Create relationships (dependencies, associations, etc.)
- `create_part` - Create part properties for composite structures
- `set_type` - Set types for parameters and properties
- `saf_create_diagram` - Create SAF-conformant UML diagrams
- `saf_add_association_paths` - Add composition/association lines to diagrams

### Using the MCP Server

**To create UML elements:**

```groovy
// Create a package
create_element(
    type='Package',
    name='MyPackage',
    parentId='<parent-package-id>',
    documentation='Package description'
)

// Create a class in the package
create_element(
    type='Class',
    name='MyClass',
    parentId='<package-id>',
    documentation='Class description'
)

// Create an operation on the class
create_element(
    type='Operation',
    name='myMethod',
    parentId='<class-id>',
    documentation='Method description'
)
```

**To create relationships:**

```groovy
// Create dependency
create_relationship(
    type='dependency',
    sourceId='<client-class-id>',
    targetId='<supplier-class-id>'
)

// Create composition
create_relationship(
    type='composition',
    sourceId='<whole-class-id>',
    targetId='<part-class-id>'
)
```

**To create diagrams:**

```groovy
// Create class diagram
saf_create_diagram(
    name='MyClass Diagram',
    parentId='<package-id>',
    diagramType='Class Diagram',
    elementIds=['<class-id>', '<class-id>', ...]
)
```

**Type Management:**

- Create custom types in a `Types` package to avoid duplicates
- Use standard UML types (String, Integer, Boolean) from UML Standard Profile when available
- Apply types to parameters using `set_type(elementId='<param-id>', typeId='<type-id>')`

### Workflow Integration

1. **Phase 1 (Codebase Analysis)**: Use `create_element(type='Package', ...)` to create package structure
2. **Phase 2 (Class Analysis)**: Use `create_element(type='Class', ...)` to create classes
3. **Phase 3 (Behavior Analysis)**: Use `create_element(type='Operation', ...)` to create operations
4. **Phase 4 (Architecture Synthesis)**: Use `saf_create_diagram()` to create final diagrams
5. **Phase 5 (Learnings)**: Document findings; diagrams remain in Cameo model

**Best Practices:**
- Always verify element IDs before creating relationships
- Create types in a dedicated Types package
- Use `saf_create_diagram` for SAF-conformant diagrams
- Call `saf_add_association_paths` after creating relationships to visualize them

### Example Session with MCP Server

```
User: Let's reverse engineer this codebase using the Cameo MCP server

Agent: I'll use the Cameo MCP Server to create UML elements.

### Step 1: Create Package Structure
- create_element(type='Package', name='domain', parentId='...')
- create_element(type='Package', name='service', parentId='...')

### Step 2: Create Classes
- create_element(type='Class', name='UserService', parentId='...')
- create_element(type='Class', name='User', parentId='...')

### Step 3: Create Operations
- create_element(type='Operation', name='createUser', parentId='UserService')
- create_element(type='Operation', name='getUser', parentId='UserService')

### Step 4: Create Parameters
- create_element(type='Parameter', name='username', parentId='createUser')
- set_type(elementId='username-param-id', typeId='String-type-id')

### Step 5: Create Relationships
- create_relationship(type='dependency', sourceId='UserService', targetId='User')
- saf_add_association_paths(diagramId='...', containerId='...')

### Step 6: Create Diagram
- saf_create_diagram(name='UserService Diagram', diagramType='Class Diagram', ...)

Summary: Created 5 classes, 8 operations, 3 dependencies, 1 diagram
```

// Create class
create_element(type='Class', name='ClassName', parentId='parentId')

// Create operation
create_element(type='Operation', name='methodName', 
    parentId='<class-id>', 
    documentation='Description')

// Create parameter
create_element(type='Parameter', name='paramName', 
    parentId='<operation-id>',
    documentation='Parameter description')

// Set type for parameter
set_type(elementId='<param-id>', typeId='<type-id>')

// Create dependency
create_relationship(type='dependency', 
    sourceId='<class-id>', 
    targetId='<dependency-id>')

// Create composition
create_relationship(type='composition', 
    sourceId='<whole-id>', 
    targetId='<part-id>')
```

### UML Diagram Creation

```groovy
// Create class diagram
saf_create_diagram(
    name='ClassName Diagram',
    parentId='<package-id>',
    diagramType='Class Diagram',
    elementIds=['<class-id>', '<class-id>', ...]
)

// Create sequence diagram
saf_create_diagram(
    name='Workflow Sequence',
    parentId='<package-id>',
    diagramType='Sequence Diagram',
    elementIds=['<lifeline-id>', '<lifeline-id>', ...]
)
```

## Common Patterns to Recognize

### Design Patterns

1. **Singleton**
   - One instance per application
   - Lazy or eager initialization
   - Thread-safe or not

2. **Factory**
   - Creates objects without specifying concrete class
   - Abstract factory for families of objects

3. **Observer**
   - Subject/Observer pattern
   - Event-driven communication

4. **Strategy**
   - Interchangeable algorithms
   - Encapsulates behavior

5. **Decorator**
   - Adds behavior dynamically
   - Wraps existing objects

### Code Smells to Watch

1. **Long Methods** - Break into smaller methods
2. **Large Classes** - Extract classes
3. **Feature Envy** - Move methods to classes they use
4. **Data Clumps** - Extract classes for grouped data
5. **Primitive Obsession** - Use objects instead of primitives

## Limitations and Caveats

1. **Static Analysis Only**
   - Cannot understand runtime behavior without execution
   - May miss dynamic dependencies
   - Cannot see test scenarios without test code

2. **Missing Context**
   - May not understand business rules
   - May miss historical decisions
   - May not know why certain design choices were made

3. **Incomplete Coverage**
   - May miss configuration files
   - May not understand environment setup
   - May miss documentation

4. **Tool Limitations**
   - UML tools may not support all patterns
   - Some languages have no direct UML equivalents
   - May need custom profiles

## Quality Checklist

Before finalizing documentation:

- [ ] All diagrams reference existing code
- [ ] Relationships are verified in code
- [ ] Key classes are documented
- [ ] Business rules are captured
- [ ] Design decisions are explained
- [ ] Recommendations are actionable
- [ ] Terminology is consistent
- [ ] No duplicate type definitions
- [ ] Types are organized logically
- [ ] Documentation is up-to-date with code

## Integration with Existing Workflows

### For New Codebases
1. Run Phase 1-5 sequentially
2. Create architecture review document
3. Generate backlog from recommendations
4. Schedule follow-up sessions

### For Existing Documentation
1. Compare reverse-engineered diagrams with existing docs
2. Update discrepancies
3. Fill gaps in existing documentation
4. Archive old documentation

### For Continuous Improvement
1. Add new learnings to knowledge base
2. Update style guide based on findings
3. Create training materials from patterns found
4. Establish coding standards from good practices found

## Example Session

```
User: Let's reverse engineer this codebase into UML

Agent: I'll guide you through the reverse engineering process.

### Step 1: Initial Assessment
- Scanning file structure...
- Found 45 Java files in 5 packages
- Identified main entry point: App.java
- Noted dependencies: Spring, Hibernate, JPA

### Step 2: Package Analysis
- Creating package diagram...
- Identified 5 logical packages:
  - com.example.domain
  - com.example.service
  - com.example.repository
  - com.example.model
  - com.example.config

### Step 3: Key Class Analysis
- Analyzing core classes...
- Found 12 domain classes
- Identified 8 service classes
- Noted 3 repository interfaces
- Created class diagram with key relationships

### Step 4: Behavior Analysis
- Tracing main workflow...
- Identified user registration flow
- Created sequence diagram for registration
- Mapped state transitions in User entity

### Step 5: Documentation Generation
- Creating architecture document...
- Writing class documentation...
- Generating recommendations...

### Summary
- Created 5 UML diagrams
- Documented 25 classes
- Identified 8 design patterns
- Found 3 code smells
- Generated 5 refactoring recommendations

Would you like me to expand on any section or create additional diagrams?
```

## Related Skills

- **Code Review**: Use reverse engineering for pre-review analysis
- **Technical Writing**: Create documentation from reverse-engineered content
- **Architecture Design**: Use learnings for new architecture decisions
- **Legacy Migration**: Prepare migration plans from reverse engineering

## Version History

- **v1.0** (2026-09-19): Initial version
  - Created structured workflow
  - Added documentation templates
  - Included best practices
  - Added example session