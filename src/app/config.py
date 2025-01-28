# Common configuration of the application

Config = {
    "histogram_horizontal": True,
    "default_granularity": 16,
    "cache_dir": "./data/_cache",
    "data_dir": "./data",
    "data_file_name": "contact_data.txt",
    "css": """
        <style>
            .st-eb {
                background-color: #f0f0f0;
                padding: 1rem;
                border-radius: 0.5rem;
                margin: 1rem 0;
            }
            .st-eb a {
                color: #000;
                text-decoration: none;
            }
            .st-eb a:hover {
                text-decoration: underline;
            }
        </style>
    """,
}
