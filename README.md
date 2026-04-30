# gocode

A code programming tool that automates the entire development process, from project initialization to acceptance testing.

## Features

- **Project Initialization**: Create standardized project structure in specified workspace directory
- **Requirement Analysis**: Deep analysis and decomposition of user requirements using local LM Studio service
- **Resource Acquisition**: Automatic web crawling for project resources with fallback to LM Studio creation
- **Development Implementation**: Modular planning and code generation
- **Testing and Verification**: Unit testing, boundary condition testing, and system integration testing
- **Acceptance**: Generate acceptance reports to confirm product functionality

## Installation

```bash
# Clone the repository
git clone https://github.com/ShiAnLiu/gocode.git
cd gocode

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Usage

### Command Line Interface

```bash
# Initialize a new project
gocode init --workspace /path/to/workspace --project-name myproject

# Analyze requirements
gocode analyze --requirements "Build a web application for task management"

# Start development process
gocode develop

# Run tests
gocode test

# Generate acceptance report
gocode accept
```

### Graphical User Interface

```bash
# Start the GUI
gocode gui
```

## Configuration

Configuration files are located in the `config` directory. You can modify the following settings:

- `lm_studio_config.json`: LM Studio API configuration
- `security_config.json`: Security settings and file system access restrictions
- `project_templates.json`: Project templates for different types of projects

## Security

- Strictly limits file system operations to the workspace directory
- Implements file access permission control
- Only allows LM Studio API calls during requirement analysis and resource acquisition phases

## Supported Platforms

- Windows
- macOS
- Linux

## Documentation

For detailed documentation, please refer to the `docs` directory or visit our [GitHub Pages](https://github.com/ShiAnLiu/GoCode.git).

## License

MIT License
