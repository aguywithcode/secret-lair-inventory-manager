# MTG Inventory Manager - Development Roadmap

This document outlines the planned features and improvements for the MTG Inventory Manager project.

## Short-term Goals (1-3 months)

### User Experience Improvements
- Add sorting and filtering options for Secret Lairs in the web interface
- Implement pagination for large numbers of Secret Lair drops
- Create a dark mode option for the web interface
- Add export functionality (CSV, PDF) for Secret Lair data

### Data Enhancements
- Add historical price tracking for cards
- Include release date information for Secret Lairs
- Store and display card rarity information
- Add card type categorization (creature, instant, etc.)

## Medium-term Goals (3-6 months)

### Collection Management
- Implement user accounts and authentication
- Create personal collection tracking functionality
- Add ability to mark Secret Lairs as owned/wanted
- Develop a dashboard showing collection value and statistics

### Price Analysis
- Implement price trend visualization
- Add price alerts for significant changes
- Create price history charts for each card
- Calculate ROI (Return on Investment) for Secret Lairs

### Personal Inventory Management
- Build a card inventory tracking system with quantities and conditions
- Implement deck building functionality with drag-and-drop interface
- Create deck statistics (mana curve, color distribution, card types)
- Support for different formats (Standard, Modern, Commander, etc.)
- Deck sharing and exporting to popular platforms (Moxfield, Archidekt)
- Card wishlist functionality with price tracking

## Long-term Goals (6+ months)

### Expanded Product Support
- Add support for other special products beyond Secret Lairs:
  - Commander decks
  - Prerelease kits
  - Collector boosters
  - Special edition sets
- Implement a unified product browser across all product types

### Advanced Features
- Create an API for third-party applications
- Develop a mobile application
- Add card condition tracking for collection items
- Implement wishlist functionality with price notifications
- Add community features (comments, ratings, reviews)

### Azure Cloud Infrastructure
- Migrate application to Azure App Service for scalable hosting
- Convert data initialization scripts to Azure Functions or WebJobs
  - Set up nightly scheduled runs to update card data automatically
  - Implement webhook triggers for immediate updates when new Secret Lairs are announced
- Migrate data storage from local JSON files to Azure Cosmos DB
  - Design optimized data schema for card and collection queries
  - Implement caching strategies for frequently accessed data
- Convert RESTful APIs to Azure Functions
  - Create serverless endpoints for data retrieval
  - Implement authentication using Azure Active Directory B2C
- Set up Azure CDN for caching static assets and images
- Implement Azure Application Insights for monitoring and analytics
- Create CI/CD pipelines with GitHub Actions or Azure DevOps

### Development Environment
- Configure standardized development environment using Dev Containers
- Set up automated testing environment with pytest
- Implement pre-commit hooks for code quality checks
- Create documentation generation pipeline
- Configure infrastructure-as-code using Terraform for Azure resources

## Community Suggestions

We welcome community input on prioritizing these features or suggesting new ones. Please submit your ideas via GitHub issues with the "feature request" label.

## Contribution Opportunities

For developers interested in contributing, the following areas are good starting points:

- Web interface improvements
- Data visualization components
- API development
- Performance optimizations
- Automated testing

See our [Contributing Guidelines](README.md#contributing) for more information on how to get involved.
