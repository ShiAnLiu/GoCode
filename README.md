# gocode

A code programming tool that automates the entire development process, from project initialization to acceptance testing.

## Features

- **Project Initialization**: Create standardized project structure in specified workspace directory
- **Requirement Analysis**: Deep analysis and decomposition of user requirements using configurable AI providers (LM Studio, Ollama, OpenAI, Anthropic, etc.)
- **Resource Acquisition**: Automatic web crawling for project resources with fallback to AI creation
- **Development Implementation**: Modular planning and code generation
- **Testing and Verification**: Unit testing, boundary condition testing, and system integration testing
- **Acceptance**: Generate acceptance reports to confirm product functionality

## Installation

```bash
# Clone the repository
git clone https://github.com/ShiAnLiu/GoCode.git
cd GoCode

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
gocode analyze --requirements "Build a web application for task management" --output requirements.md

# Acquire project resources
gocode acquire --requirements "Build a web application for task management"
gocode acquire --requirements "Build a web application for task management" --output-dir resources

# Start development process
gocode develop --project-dir /path/to/workspace/myproject --requirements "Build a web application for task management"

# Run tests
gocode test --project-dir /path/to/workspace/myproject

# Generate acceptance report
gocode accept --project-dir /path/to/workspace/myproject --requirements "Build a web application for task management"
```

### Graphical User Interface

```bash
# Start the GUI
gocode gui
```

## Configuration

Configuration files are located in the `config` directory. You can modify the following settings:

- `api_config.json`: API provider configuration (supports LM Studio, Ollama, OpenAI, Anthropic, etc.)
- `security_config.json`: Security settings and file system access restrictions
- `project_templates.json`: Project templates for different types of projects

## Security

- Strictly limits file system operations to the workspace directory
- Implements file access permission control via `SecurityManager`
- `safe_open`, `safe_mkdir`, `safe_remove`, `safe_copy`, and `safe_rename` wrappers prevent path traversal
- API calls are only made during requirement analysis and resource acquisition phases
- All external HTTP requests respect configurable timeout values

## Supported Platforms

- Windows
- macOS
- Linux

## Documentation

For detailed documentation, please refer to the `docs` directory or visit our [GitHub Pages](https://ShiAnLiu.github.io/GoCode).

## License

MIT License
