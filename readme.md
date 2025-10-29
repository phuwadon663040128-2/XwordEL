
<p align="center">
    <img src="XwordEL/mystaticfiles/img/logo1.1.png" width="100">
</p>
<p align="center">
    <h1 align="center">XWORDEL-PROJECT</h1>
</p>
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>

- [ Overview](#overview)
- [ Features](#features)
- [ Repository Structure](#repository-structure)
- [ Modules](#modules)
- [Credit](#credit)
- [ License](#license)
</details>
<hr>


## Overview

The XWORDEL-PROJECT, or XwordEL (standing for Crossword for English Learning), is a crossword web application aimed at combining crossword puzzle enjoyment with English vocabulary learning. Developed using Django, HTMX, HTML, CSS, and JavaScript, this platform offers an interactive experience for improving English vocabulary.


---

  

## Features
Key features of the XWORDEL-PROJECT include:

- Meaning as Clue: We use  [dictionary APIs](#credit) to convert the meanings of words into clues for the crossword puzzles.

- Dynamic Crossword Puzzle Generation and Gameplay: Each puzzle is [algorithmically](#credit) generated to ensure a unique challenge every time. Our intuitive interface facilitates seamless gameplay, enhancing user engagement.

  

- File to Crossword Puzzle: Have words in a text or PDF file? [OCR](#credit) and [crossword generation algorithm](#credit) can convert those words into crossword puzzles.

  

- Responsive Design: The XWORDEL-PROJECT provides a seamless experience across all devices, whether you're on a desktop at home or solving puzzles on your phone.

---
## Related repo

to run this project, you may need these 2 repo
- https://github.com/ct255/spaCy-wordSpliter
- https://github.com/ct255/esayOCR-API
---


##  Repository Structure

```sh
└── XwordEL-project/
    └── XwordEL
        ├── Procfile
        ├── XwordApp
        ├── XwordAuth
        ├── XwordEL
        ├── XwordHome
        ├── manage.py
        ├── requirements.txt
        ├── runtime.txt
        ├── static
        ├── staticfiles
        └── templates
```

---

##  Modules

<details closed><summary>XwordEL</summary>

| File                                                                                              | Summary                                                                                                                                                                                                                                                        |
| ---                                                                                               | ---                                                                                                                                                                                                                                                            |
| [runtime.txt](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/runtime.txt)           | Specifies Python version for runtime environment in XwordEL project.                                                                                                                                                                                           |
| [Procfile](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/Procfile)                 | Initiates web server with specified parameters to handle incoming requests efficiently, utilizing Gunicorn and Djangos migration capabilities.                                                                                                                 |
| [manage.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/manage.py)               | Executes administrative tasks in Django, setting environment variables and handling command-line operations for the XwordEL project.                                                                                                                           |
| [requirements.txt](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/requirements.txt) | Specifies required Python packages for the XwordEL project. Facilitates seamless integration and functionality across various project components. Reflects dependencies essential for efficient execution and performance within the repositorys architecture. |

</details>

<details closed><summary>XwordEL.XwordHome</summary>

| File                                                                                          | Summary                                                                                                                                                                                                    |
| ---                                                                                           | ---                                                                                                                                                                                                        |
| [views.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordHome/views.py)   | Renders the home page view for XwordEL project. Displays content in the home.html template. Supports seamless user experience within repository's application architecture.                                |
| [models.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordHome/models.py) | Defines database models for the XwordHome app within the XwordEL project. Includes essential data structures for managing content and interactions specific to the home section of the crossword platform. |
| [admin.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordHome/admin.py)   | Registers models for Django administration in the XwordHome app.                                                                                                                                           |
| [apps.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordHome/apps.py)     | Defines app configuration for XwordHome within the Django project, specifying default database field and app name. Key contribution for proper functioning and organization within the XwordEL repository. |
| [tests.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordHome/tests.py)   | Verifies Django TestCase functionalities for XwordHome module within the XwordEL repository.                                                                                                               |
| [urls.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordHome/urls.py)     | Defines URL routing for the home page view function in XwordHome module within XwordEL repository.                                                                                                         |

</details>

<details closed><summary>XwordEL.templates</summary>

| File                                                                                                          | Summary                                                                                                                                                                                                                                                                                      |
| ---                                                                                                           | ---                                                                                                                                                                                                                                                                                          |
| [login.html](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/templates/login.html)               | Renders a login form within the user interface. Displays login fields for username and password, along with error messages. Allows users to log in and navigate to the signup page if not registered. Integrates icon fonts for visual elements.                                             |
| [home.html](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/templates/home.html)                 | Displays dynamic navigation based on user authentication status. Showcases team members info with cards. Links to various pages seamlessly. Engages users interaction for account management and gameplay. Effortlessly integrates into XwordEL project's frontend structure.                |
| [signup.html](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/templates/signup.html)             | Enables user signup functionality by rendering a form with error message handling and links to login page. Utilizes userformbase.html for design consistency and ionicons for visual elements, providing a seamless signup experience in the XwordEL project.                                |
| [profile.html](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/templates/profile.html)           | Displays user profile with message alerts, options to download played words in Thai/English, and checkboxes for word deletion. Implements CSRF protection and interactions via buttons. Includes ionicons for visual appeal.                                                                 |
| [userformbase.html](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/templates/userformbase.html) | Enhances user experience through custom styling and interactivity. Dynamically loads assets and scripts, setting dynamic title defaults. Implements particle background animation for visual appeal.                                                                                         |
| [gameoptions.html](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/templates/gameoptions.html)   | Implements dynamic game options selection and file uploading functionality.-Interacts with user inputs to modify hidden form values.-Utilizes htmx for AJAX loading and dynamic content display.-Enhances user experience with smooth scrolling and visual feedback.                         |
| [XwordGame.html](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/templates/XwordGame.html)       | Implements interactive crossword game UI with dynamic loading bar. Handles form submissions for game progress and congratulatory messages upon completion. Incorporates htmx events for user engagement and triggers new crossword generation. Allows easy navigation back to the home page. |
| [base.html](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/templates/base.html)                 | Customizes CSS styles and meta tags dynamically based on URL paths for the XwordEL projects front-end interface. Implements responsive design and essential metadata for SEO and sharing. Enhances user experience through optimized resource loading.                                       |
| [endgame.html](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/templates/endgame.html)           | Automates redirection to the options page upon completion of all words in the wordlist. Essential for seamless user experience and progression within XwordEL applications gameplay flow.                                                                                                    |

</details>

<details closed><summary>XwordEL.XwordApp</summary>

| File                                                                                                                 | Summary                                                                                                                                                                                                                                                                                                          |
| ---                                                                                                                  | ---                                                                                                                                                                                                                                                                                                              |
| [views.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordApp/views.py)                           | Generates crossword puzzles dynamically, validates and fills user input, and highlights correct answers. Handles word placements, numbering, and hints. Utilizes ASCII grids for puzzle layout and tracks completion progress. Manages word meanings and error handling effectively within the application flow. |
| [words_process.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordApp/words_process.py)           | Processes text through an API to derive base words for a project in the XwordEL repository. Handles API communication, error management, and response construction for base word extraction.                                                                                                                     |
| [models.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordApp/models.py)                         | Defines database models for common words, user played words with Thai and English meanings, and all English and Thai words. Facilitates data storage and retrieval in XwordEL project for word-related functionalities.                                                                                          |
| [admin.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordApp/admin.py)                           | Registers models for admin interface in XwordApp, facilitating easy data management. Key to repositorys Django-based architecture, ensuring seamless backend administration.                                                                                                                                     |
| [views2.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordApp/views2.py)                         | Displays OCR checkbox if API is accessible; shows OCR API NOT AVAILABLE tooltip if API is unavailable. Authenticated users access Spacy API endpoint.                                                                                                                                                            |
| [pdf_processer.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordApp/pdf_processer.py)           | Processes uploaded PDF files, extracting text content. Utilizes OCR API for text extraction, handling errors gracefully. Supports parallel processing for efficiency. Dynamically determines file type for processing, alerting if unsupported.                                                                  |
| [apps.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordApp/apps.py)                             | Registers the XwordApp configuration within the Django framework. Identifies the default database field and specifies the app name.                                                                                                                                                                              |
| [tests.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordApp/tests.py)                           | Verifies Django app functionality with TestCase.                                                                                                                                                                                                                                                                 |
| [getclue.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordApp/getclue.py)                       | Retrieves word definitions from Longdo and Free Dictionary APIs, handling different search modes. Extracts and formats meanings for each word queried, utilizing threading for parallel processing. Contributes language support to the repositorys word-based functionality.                                    |
| [urls.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordApp/urls.py)                             | Game UI, options, file upload, and API endpoints for OCR and Spacy. Supports game interaction, configuration, OCR services, and NLP features within the XwordEL projects Django web application.                                                                                                                 |
| [crossword_algo_mod.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordApp/crossword_algo_mod.py) | Generates crosswords with optimized placements, aligning words without overlaps. Handles diverse word lists efficiently, providing insights into placed and unplaced words. Outputs grid representations and highlights missing placements.                                                                      |
| [forms.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordApp/forms.py)                           | Enables user interaction for crossword session reset and validation via form input fields.                                                                                                                                                                                                                       |

</details>

<details closed><summary>XwordEL.XwordApp.migrations</summary>

| File                                                                                                                                                                                                    | Summary                                                                                                                                                                                                                                                     |
| ---                                                                                                                                                                                                     | ---                                                                                                                                                                                                                                                         |
| [0002_all_eng_words_all_thai_words_common_word_and_more.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordApp/migrations/0002_all_eng_words_all_thai_words_common_word_and_more.py) | Introduces multiple model creations for English and Thai words, along with user-played words, and eliminates the Test_class_person model. Enhances the XwordApp's data structure for word storage and gameplay functionality within the XwordEL repository. |
| [0001_initial.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordApp/migrations/0001_initial.py)                                                                                     | Creates Test_class_person model with name and age fields. No dependencies. Part of the Django project's XwordApp module. Contributing to the database schema setup for the application.                                                                     |

</details>

<details closed><summary>XwordEL.XwordApp.scripts</summary>

| File                                                                                                                                   | Summary                                                                                                                                                                                                                                  |
| ---                                                                                                                                    | ---                                                                                                                                                                                                                                      |
| [add_word.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordApp/scripts/add_word.py)                               | Populates the common_word table by reading a file of 1000 most common words. Deletes existing entries before adding new words. This script supports data integrity in the XwordEL repository's architecture.                             |
| [1000-most-common-words.txt](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordApp/scripts/1000-most-common-words.txt) | Lists the 1000 most common English words. Helpful for language-based functionalities within the app.                                                                                                                                     |
| [filter.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordApp/scripts/filter.py)                                   | Filters common words from a file based on pre-defined blacklist, deduplicates, and removes short/non-alphabetic words. Enhances file by saving optimized wordlist. Contributing to XwordEL projects functionality by refining word data. |

</details>

<details closed><summary>XwordEL.XwordEL</summary>

| File                                                                                            | Summary                                                                                                                                                                                                                                                       |
| ---                                                                                             | ---                                                                                                                                                                                                                                                           |
| [wsgi.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordEL/wsgi.py)         | Exports the WSGI callable as application, facilitating Django project deployment. Sets Django settings module and fetches WSGI application for XwordEL project. Vital for web server compatibility.                                                           |
| [settings.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordEL/settings.py) | Defines Django settings, loads environment variables, and configures middleware and databases. Sets up static files and URLs. Tests connection to external APIs. Crucial for configuring the XwordEL projects core functionality and integrations.            |
| [test_api.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordEL/test_api.py) | Verifies API availability by connecting to specified URLs with a timeout setting. Uses color-coded messages to indicate API status, aiding in determining API functionality within the Django project.                                                        |
| [urls.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordEL/urls.py)         | Defines URL routing for XwordEL project by mapping URLs to respective views using Djangos urlpatterns. Includes routes for admin panel, XwordApp functionality, homepage, and authentication. Central piece connecting various modules in the Django project. |
| [asgi.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordEL/asgi.py)         | Configures ASGI for the XwordEL project by exposing the callable application. Sets the DJANGO_SETTINGS_MODULE and retrieves the ASGI application for deployment.                                                                                              |

</details>

<details closed><summary>XwordEL.XwordAuth</summary>

| File                                                                                          | Summary                                                                                                                                                                                                                                                                                                                          |
| ---                                                                                           | ---                                                                                                                                                                                                                                                                                                                              |
| [views.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordAuth/views.py)   | Implements user authentication and signup flows. Handles login, logout, and signup requests using Djangos authentication system. Ensures session expiry after browser closure. Displays appropriate messages for success and failure scenarios. Provides essential functionality for user management within the XwordEL project. |
| [models.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordAuth/models.py) | Defines database models for authentication-related data in Django. Establishes structure for user authentication and authorization. Key features include user profile, permissions, and access control settings. Essential for maintaining security and user management capabilities within the application.                     |
| [admin.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordAuth/admin.py)   | Registers Django models in the admin interface for the XwordAuth component in the XwordEL repository.                                                                                                                                                                                                                            |
| [views2.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordAuth/views2.py) | Analyzes and manages user played words for Thai and English languages. Provides functionality to delete and download users played words. Calculates and displays word count and percentage for each language. Key features include deletion, download, and stats display for played words.                                       |
| [apps.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordAuth/apps.py)     | Defines the configuration for XwordAuth app within the XwordEL project. Initialized with default settings for Django app. It plays a crucial role in managing app-specific behaviors in the project architecture.                                                                                                                |
| [tests.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordAuth/tests.py)   | Verifies Django authentication functionality. Tests user authentication processes.                                                                                                                                                                                                                                               |
| [urls.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordAuth/urls.py)     | Defines authentication and user profile URLs, facilitating login, logout, signup, and profile viewing. Supports downloading played words in English and Thai. Integrates with the XwordEL projects architecture for seamless user management.                                                                                    |
| [forms.py](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/XwordAuth/forms.py)   | Implements user creation and word management forms with customized field attributes. It enhances user experience by disabling autocomplete and offers options for deleting and downloading played words in Thai and English, contributing to user data control within the XwordEL platform.                                      |

</details>

<details closed><summary>XwordEL.staticfiles</summary>

| File                                                                                                                                | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ---                                                                                                                                 | ---                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| [modal.js](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/staticfiles/modal.js)                                       | Implements modal functionality to display and hide content. Toggles modal display based on user interaction. Enhances user experience in the XwordEL projects frontend.                                                                                                                                                                                                                                                                          |
| [htmx.min.js](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/staticfiles/htmx.min.js)                                 | Implements functionality to trigger AJAX requests, handle responses, and update the DOM dynamically. Manages sending, handling, and displaying data fetched from the server without page reloads or user intervention.                                                                                                                                                                                                                           |
| [django-htmx.js](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/staticfiles/django-htmx.js)                           | Monitors and handles debug mode issues in dynamic content loading for the XwordEL Django project. Stops processing erroneous responses, replaces content dynamically, and ensures proper script execution to maintain project stability.                                                                                                                                                                                                         |
| [staticfiles.json](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/staticfiles/staticfiles.json)                       | Maps static file paths to versioned file paths in a JSON format for efficient static file handling and version control within the repositorys architecture.                                                                                                                                                                                                                                                                                      |
| [script.js](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/staticfiles/script.js)                                     | Implements smooth scrolling and highlighting features for crossword interaction. Enhances user experience by intelligently navigating input fields along axes. Identifies and highlights related clues, improving user engagement. Addresses potential code repetitions for a seamless crossword-solving experience.                                                                                                                             |
| [userform.js](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/staticfiles/userform.js)                                 | Handles user input focus and blur events, displaying help text dynamically. Also, enables page redirection to the home page on button click.                                                                                                                                                                                                                                                                                                     |
| [home.js](https://github.com/ct255/XwordEL-project/blob/master/XwordEL/staticfiles/home.js)                                         | Implements smooth scrolling and element reveal animations for the XwordEL projects frontend. Enhances user experience on scrolling and interaction with the websites sections.                                                                                                                                                                                                                                                                   |
</details>

---
## Credit
<b>Thanks to all of these projects</b>
- Django : https://www.djangoproject.com
- HTMX : https://htmx.org
- spaCy : https://spacy.io/
- FastAPI : https://fastapi.tiangolo.com/
- Crossword Creation Algorithm : https://github.com/dnoegel/crossword-generator
- easy-OCR : https://github.com/JaidedAI/EasyOCR
- Longdo Dict : https://dict.longdo.com
- Free Dictionary API : https://dictionaryapi.dev

---



##  License

This project is protected under the GNU General Public License v3.0. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/gpl-3.0/) file.


