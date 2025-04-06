document.addEventListener('DOMContentLoaded', function() {
    // Set current year in footer
    document.getElementById('year').textContent = new Date().getFullYear();

    // Header scroll effect
    const header = document.querySelector('header');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Project data - Replace with your actual projects
    const projects = [
        {
            title: "Calculator App",
            description: "A simple calculator app built with HTML, CSS, and JavaScript.",
            image : "Calculator.jpg",
            githubUrl: "https://github.com/AadityaSaxena20/Calculator",
            liveDemo: "https://aadityasaxena20.github.io/Calculator/"
        },
        {
            title: "Weather App",
            description: "Real-time weather application with location detection.",
            image: "weather.jpg",
            githubUrl: "https://github.com/AadityaSaxena20/Weather-App",
            liveDemo: "https://aadityasaxena20.github.io/Weather-App/"
        },
        {
            title: "Click the Circle!",
            description: "Fun game where you click on circles that appear randomly.",
            image: "game.jpg",
            githubUrl: "https://github.com/AadityaSaxena20/Click-the-Circle",
            liveDemo: "https://aadityasaxena20.github.io/Click-the-Circle/"
        },
        {
            title: "To-Do List",
            description: "A simple to-do list application to manage tasks.",
            image: "todo.jpg",
            githubUrl: "https://github.com/AadityaSaxena20/To-Do-List",
            liveDemo: "https://aadityasaxena20.github.io/To-Do-List/"
        },
        {
            title: "Password Strength Indicator",
            description: "A tool to check the strength of your passwords.",
            image: "password.jpg",
            githubUrl: "https://github.com/AadityaSaxena20/Password-Strength-Indicator",
            liveDemo: "https://aadityasaxena20.github.io/Password-Strength-Indicator/"
        }
    ];

    // Load projects dynamically
    const projectsContainer = document.getElementById('projects-container');
    
    projects.forEach(project => {
        const projectCard = document.createElement('div');
        projectCard.className = 'project-card';
        
        projectCard.innerHTML = `
            <div class="project-image">
                <img src="${project.image}" alt="${project.title}">
            </div>
            <div class="project-info">
                <h3>${project.title}</h3>
                <p>${project.description}</p>
                <div class="project-links">
                    <a href="${project.githubUrl}" target="_blank" rel="noopener noreferrer">View Code</a>
                    <a href="${project.liveDemo}" target="_blank" rel="noopener noreferrer">Live Demo</a>
                </div>
            </div>
        `;
        
        projectsContainer.appendChild(projectCard);
    });

    // Form submission handling
    const contactForm = document.getElementById('contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;
            
            // Here you would typically send the form data to a server
            // For this example, we'll just log it and show an alert
            console.log({ name, email, message });
            
            alert('Thank you for your message! I will get back to you soon.');
            contactForm.reset();
        });
    }

    // Animation on scroll
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.project-card, .about-content, .contact-form');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            
            if (elementPosition < screenPosition) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };

    // Set initial state for animation
    document.querySelectorAll('.project-card, .about-content, .contact-form').forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });

    window.addEventListener('scroll', animateOnScroll);
    // Trigger once on load in case elements are already in view
    animateOnScroll();
});
