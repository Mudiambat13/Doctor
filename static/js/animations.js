import gsap from "gsap";

// Timeline principale
const tl = gsap.timeline();

// Animation d'entrée de la page
tl.from('#app', {
    duration: 1,
    opacity: 0,
    y: 50,
    ease: 'power3.out'
});

// Animation du menu latéral
tl.from('.sidebar', {
    duration: 0.8,
    x: -300,
    opacity: 0,
    ease: 'power4.out'
}, "-=0.5");

// Animation des cartes
gsap.from('.card', {
    duration: 0.8,
    scale: 0.8,
    y: 100,
    opacity: 0,
    stagger: 0.2,
    ease: 'back.out(1.7)',
    scrollTrigger: {
        trigger: '.card',
        start: 'top bottom',
        toggleActions: 'play none none reverse'
    }
});

// Animation des boutons
const buttons = document.querySelectorAll('.btn-hover');
buttons.forEach(btn => {
    btn.addEventListener('mouseenter', () => {
        gsap.to(btn, {
            scale: 1.05,
            duration: 0.3,
            backgroundColor: '#2563eb',
            color: 'white',
            ease: 'power2.out'
        });
    });

    btn.addEventListener('mouseleave', () => {
        gsap.to(btn, {
            scale: 1,
            duration: 0.3,
            backgroundColor: '#ffffff',
            color: '#1f2937',
            ease: 'power2.out'
        });
    });
});

// Animation des notifications
gsap.from('.notification', {
    duration: 0.5,
    x: -100,
    opacity: 0,
    ease: 'elastic.out(1, 0.8)',
    stagger: 0.2
});

// Animation du contenu au scroll
gsap.utils.toArray('.animate-on-scroll').forEach(element => {
    gsap.from(element, {
        scrollTrigger: {
            trigger: element,
            start: 'top 80%',
            toggleActions: 'play none none reverse'
        },
        y: 50,
        opacity: 0,
        duration: 1,
        ease: 'power3.out'
    });
});

// Animation des formulaires
gsap.from('form', {
    duration: 1,
    y: 30,
    opacity: 0,
    ease: 'power3.out'
}); 