// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Flash message auto-hide
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 3000);
    });
});

// Form validation
const contactForm = document.querySelector('.contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        const emailInput = document.querySelector('#email');
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (!emailPattern.test(emailInput.value)) {
            e.preventDefault();
            alert('Please enter a valid email address');
        }
    });
}

// Project card hover effect
const projectCards = document.querySelectorAll('.project-card');
projectCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-5px)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });
});

// Skill bar animation
function animateSkillBars() {
    const skillLevels = document.querySelectorAll('.skill-level');
    skillLevels.forEach(level => {
        const width = level.style.width;
        level.style.width = '0';
        setTimeout(() => {
            level.style.width = width;
        }, 100);
    });
}

// Run skill bar animation when skills section is in view
const skillsSection = document.querySelector('.skills');
if (skillsSection) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateSkillBars();
                observer.unobserve(entry.target);
            }
        });
    });
    
    observer.observe(skillsSection);
}

// Like functionality
document.querySelectorAll('.like-btn').forEach(button => {
    button.addEventListener('click', async function() {
        const projectId = this.dataset.projectId;
        try {
            const response = await fetch(`/projects/${projectId}/like`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            const data = await response.json();
            
            // Update like button appearance
            const likeCount = this.querySelector('.like-count');
            if (data.status === 'liked') {
                this.innerHTML = `<span class="like-count">${parseInt(likeCount.textContent) + 1}</span> ❤️`;
            } else {
                this.innerHTML = `<span class="like-count">${parseInt(likeCount.textContent) - 1}</span> 🤍`;
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
}); 