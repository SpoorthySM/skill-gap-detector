JOB_ROLES = {
    "Software Development Engineer": {
        "technical": [
            "Data Structures", "Algorithms", "System Design", "Object Oriented Programming",
            "Java", "Python", "C++", "SQL", "Git", "REST APIs", "Linux",
            "Dynamic Programming", "Problem Solving", "Debugging"
        ],
        "soft": ["Communication", "Teamwork", "Time Management", "Adaptability"],
        "tools": ["Git", "Docker", "AWS", "IntelliJ", "VS Code"]
    },
    "Data Scientist": {
        "technical": [
            "Python", "Machine Learning", "Statistics", "Deep Learning", "SQL",
            "Data Visualization", "Pandas", "NumPy", "Scikit-learn", "Feature Engineering",
            "EDA", "NLP", "Model Evaluation", "Data Cleaning"
        ],
        "soft": ["Analytical Thinking", "Communication", "Curiosity", "Problem Solving"],
        "tools": ["Jupyter Notebook", "Tableau", "Power BI", "TensorFlow", "PyTorch"]
    },
    "Data Analyst": {
        "technical": [
            "SQL", "Excel", "Python", "Data Visualization", "Statistics",
            "Pandas", "Tableau", "Power BI", "Data Cleaning", "EDA",
            "Business Intelligence", "Reporting", "ETL"
        ],
        "soft": ["Attention to Detail", "Communication", "Critical Thinking", "Storytelling"],
        "tools": ["Excel", "Tableau", "Power BI", "SQL", "Python"]
    },
    "Machine Learning Engineer": {
        "technical": [
            "Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
            "MLOps", "Model Deployment", "Docker", "REST APIs", "Data Structures",
            "Algorithms", "Statistics", "Feature Engineering", "NLP", "Computer Vision"
        ],
        "soft": ["Research Mindset", "Problem Solving", "Collaboration", "Documentation"],
        "tools": ["Docker", "Kubernetes", "AWS SageMaker", "MLflow", "Git"]
    },
    "Frontend Developer": {
        "technical": [
            "HTML", "CSS", "JavaScript", "React", "TypeScript", "REST APIs",
            "Responsive Design", "Git", "Performance Optimization", "Accessibility",
            "Web Security", "Testing", "Node.js"
        ],
        "soft": ["Creativity", "Attention to Detail", "Communication", "User Empathy"],
        "tools": ["VS Code", "Figma", "Chrome DevTools", "Webpack", "Git"]
    },
    "Backend Developer": {
        "technical": [
            "Python", "Java", "Node.js", "SQL", "NoSQL", "REST APIs",
            "System Design", "Microservices", "Docker", "Data Structures",
            "Algorithms", "Authentication", "Caching", "Message Queues"
        ],
        "soft": ["Problem Solving", "Attention to Detail", "Teamwork", "Documentation"],
        "tools": ["Docker", "PostgreSQL", "Redis", "Git", "Postman"]
    },
    "DevOps Engineer": {
        "technical": [
            "Linux", "Docker", "Kubernetes", "CI/CD", "AWS", "Python",
            "Bash Scripting", "Networking", "Monitoring", "Infrastructure as Code",
            "Git", "Security", "Cloud Computing"
        ],
        "soft": ["Problem Solving", "Communication", "Reliability", "Continuous Learning"],
        "tools": ["Jenkins", "Terraform", "Ansible", "Prometheus", "Grafana"]
    },
    "Quantitative Analyst (Goldman Sachs)": {
        "technical": [
            "Python", "Statistics", "Linear Algebra", "Calculus", "Probability",
            "Machine Learning", "Financial Modeling", "SQL", "C++", "Data Structures",
            "Algorithms", "Time Series Analysis", "Risk Management", "Derivatives"
        ],
        "soft": ["Analytical Thinking", "Attention to Detail", "Communication", "Ethics"],
        "tools": ["Python", "MATLAB", "Excel", "Bloomberg Terminal", "R"]
    },
    "Product Manager": {
        "technical": [
            "SQL", "Data Analysis", "Product Roadmap", "A/B Testing", "Market Research",
            "User Stories", "KPI Tracking", "Agile", "Wireframing", "Analytics"
        ],
        "soft": ["Leadership", "Communication", "Prioritization", "Strategic Thinking", "Empathy"],
        "tools": ["JIRA", "Figma", "Mixpanel", "Google Analytics", "Notion"]
    },
    "Cybersecurity Analyst": {
        "technical": [
            "Networking", "Linux", "Python", "Penetration Testing", "SIEM",
            "Cryptography", "Firewalls", "Vulnerability Assessment", "Incident Response",
            "Security Protocols", "OWASP", "Cloud Security"
        ],
        "soft": ["Analytical Thinking", "Attention to Detail", "Ethics", "Problem Solving"],
        "tools": ["Wireshark", "Metasploit", "Nmap", "Burp Suite", "Splunk"]
    }
}

SKILL_CATEGORIES = {
    "programming_languages": [
        "python", "java", "c++", "c", "javascript", "typescript", "r", "go", "rust",
        "kotlin", "swift", "scala", "matlab", "ruby", "php", "bash"
    ],
    "data_science": [
        "machine learning", "deep learning", "nlp", "computer vision", "statistics",
        "data visualization", "feature engineering", "model deployment", "mlops",
        "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras",
        "eda", "exploratory data analysis", "data cleaning", "data wrangling"
    ],
    "databases": [
        "sql", "mysql", "postgresql", "mongodb", "redis", "cassandra",
        "oracle", "sqlite", "nosql", "elasticsearch", "firebase"
    ],
    "web": [
        "html", "css", "react", "angular", "vue", "node.js", "django", "flask",
        "fastapi", "spring boot", "rest api", "graphql", "responsive design"
    ],
    "cloud_devops": [
        "aws", "azure", "gcp", "docker", "kubernetes", "ci/cd", "terraform",
        "ansible", "jenkins", "linux", "git", "microservices"
    ],
    "cs_fundamentals": [
        "data structures", "algorithms", "system design", "object oriented programming",
        "dynamic programming", "operating systems", "computer networks", "dbms",
        "computer architecture", "compilers", "oops"
    ],
    "soft_skills": [
        "communication", "teamwork", "leadership", "problem solving", "critical thinking",
        "time management", "adaptability", "creativity", "analytical thinking",
        "attention to detail", "collaboration", "presentation"
    ]
}

LEARNING_RESOURCES = {
    "Data Structures": {"platform": "LeetCode / CodeChef", "link": "https://leetcode.com/explore/learn/", "time": "4-6 weeks"},
    "Algorithms": {"platform": "GeeksforGeeks", "link": "https://www.geeksforgeeks.org/fundamentals-of-algorithms/", "time": "4-6 weeks"},
    "Machine Learning": {"platform": "Coursera (Andrew Ng)", "link": "https://www.coursera.org/learn/machine-learning", "time": "8-10 weeks"},
    "Python": {"platform": "freeCodeCamp / CS50P", "link": "https://cs50.harvard.edu/python/", "time": "3-4 weeks"},
    "SQL": {"platform": "SQLZoo / Mode Analytics", "link": "https://sqlzoo.net/", "time": "2-3 weeks"},
    "System Design": {"platform": "Grokking System Design", "link": "https://www.educative.io/courses/grokking-the-system-design-interview", "time": "6-8 weeks"},
    "Deep Learning": {"platform": "fast.ai / Coursera", "link": "https://www.fast.ai/", "time": "8-12 weeks"},
    "Docker": {"platform": "Docker Official Docs", "link": "https://docs.docker.com/get-started/", "time": "1-2 weeks"},
    "React": {"platform": "React Official Docs / Scrimba", "link": "https://react.dev/learn", "time": "4-6 weeks"},
    "Statistics": {"platform": "Khan Academy / StatQuest", "link": "https://www.khanacademy.org/math/statistics-probability", "time": "4-6 weeks"},
    "AWS": {"platform": "AWS Free Tier + Cloud Practitioner", "link": "https://aws.amazon.com/training/", "time": "4-6 weeks"},
    "Git": {"platform": "GitHub Learning Lab", "link": "https://lab.github.com/", "time": "1 week"},
    "NLP": {"platform": "Hugging Face Course", "link": "https://huggingface.co/learn/nlp-course/", "time": "6-8 weeks"},
    "Tableau": {"platform": "Tableau Public Training", "link": "https://www.tableau.com/learn/training", "time": "2-3 weeks"},
    "Power BI": {"platform": "Microsoft Learn", "link": "https://learn.microsoft.com/en-us/power-bi/", "time": "2-3 weeks"},
    "Linux": {"platform": "Linux Foundation / TryHackMe", "link": "https://training.linuxfoundation.org/", "time": "2-3 weeks"},
    "Computer Networks": {"platform": "GATE Smashers / Kunal Kushwaha", "link": "https://youtube.com/@gatesmasher", "time": "3-4 weeks"},
    "Operating Systems": {"platform": "GATE Smashers / Neso Academy", "link": "https://www.youtube.com/@nesoacademy", "time": "3-4 weeks"},
    "DBMS": {"platform": "GATE Smashers", "link": "https://www.youtube.com/@gatesmasher", "time": "3-4 weeks"},
}