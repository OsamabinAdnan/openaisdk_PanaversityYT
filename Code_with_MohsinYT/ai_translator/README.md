# AI Language Translator

A powerful and user-friendly language translation tool powered by Google's Gemini AI model. This application provides real-time translation capabilities for 27 different languages while maintaining natural language flow and context.

## Features

- Support for 27 different languages
- User-friendly interactive menu
- Real-time translation using Gemini AI
- Maintains context and natural language flow
- Error handling for user inputs
- Clean and formatted output

## Supported Languages

1. Urdu
2. French
3. Spanish
4. German
5. Chinese (Mandarin)
6. Japanese
7. Korean
8. Arabic
9. Portuguese
10. Russian
11. Hindi
12. Bengali
13. Turkish
14. Italian
15. Dutch
16. Greek
17. Hebrew
18. Malay
19. Czech
20. Romanian
21. Finnish
22. Polish
23. Swedish
24. Danish
25. Norwegian
26. Thai
27. Vietnamese

## Prerequisites

- Python 3.6 or higher
- Google Gemini API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai_translator
```

2. Install the required dependencies:
```bash
pip install agents python-dotenv
```

3. Create a `.env` file in the project root and add your Gemini API key:
```bash
GEMINI_API_KEY=your_api_key_here
```

## Usage

1. Run the translator:
```bash
python main.py
```

2. Enter the text you want to translate when prompted.

3. Select the target language by entering the corresponding number (1-27).

4. The translation will be displayed with clear formatting.

## Example

```
=== AI Language Translator ===
Enter text to translate: Hello, how are you?

=== Language Translation Menu ===
1. Urdu
2. French
[...]

Select target language (1-27): 2

Translating...

Translation to French:
----------------------------------------
Bonjour, comment allez-vous?
----------------------------------------
```

## Error Handling

The application includes robust error handling for:
- Invalid language selection
- Missing API key
- Network issues
- Invalid input types

## Technical Details

The application uses:
- Google's Gemini AI model for translations
- Python's async capabilities for better performance
- Environment variables for secure API key management
- Custom Agent architecture for handling translations

## Contributing

Feel free to fork the repository and submit pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini AI for providing the translation capabilities
- The Python community for the excellent libraries used in this project
