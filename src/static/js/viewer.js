let currentMode = 'scroll';
let currentIndex = 0;
const pages = document.querySelectorAll('.flip-page');
const totalPages = pages.length;

// Elements
const sidebarCurrent = document.getElementById('sidebar-current');
const sidebarTotal = document.getElementById('sidebar-total');
const pageSlider = document.getElementById('page-slider');

function setMode(mode) {
	currentMode = mode;

	// Update buttons
	document.querySelectorAll('.mode-btn').forEach(btn => {
		btn.classList.remove('active');
		if (btn.textContent.includes(mode === 'scroll' ? '捲動' : '翻頁')) {
			btn.classList.add('active');
		}
	});

	// Toggle views
	const scrollView = document.getElementById('scroll-view');
	const flipView = document.getElementById('flip-view');
	const pageInfo = document.getElementById('page-info');

	if (mode === 'scroll') {
		scrollView.style.display = 'flex';
		flipView.style.display = 'none';
		pageInfo.style.display = 'none';

		// Scroll to current index
		const images = scrollView.querySelectorAll('img');
		if (images[currentIndex]) {
			images[currentIndex].scrollIntoView({ behavior: 'auto', block: 'center' });
		}
	} else {
		scrollView.style.display = 'none';
		flipView.style.display = 'flex';
		pageInfo.style.display = 'none';
		showPage(currentIndex);
	}

	// Update URL without reload
	const url = new URL(window.location);
	url.searchParams.set('mode', mode);
	window.history.pushState({}, '', url);
}

function showPage(index) {
	if (index < 0) index = 0;
	if (index >= totalPages) index = totalPages - 1;

	currentIndex = index;

	pages.forEach(page => page.classList.remove('active'));
	pages[currentIndex].classList.add('active');

	// Update indicators
	document.getElementById('flip-current').textContent = currentIndex + 1;
	updateSidebar(currentIndex + 1);

	// Update buttons state
	document.querySelector('.prev-btn').style.opacity = currentIndex === 0 ? '0.5' : '1';
	document.querySelector('.next-btn').style.opacity = currentIndex === totalPages - 1 ? '0.5' : '1';
}

function updateSidebar(page) {
	if (sidebarCurrent) sidebarCurrent.textContent = page;
	if (pageSlider) {
		pageSlider.value = page;
	}

	// Update flip mode indicator as well
	const flipCurrent = document.getElementById('flip-current');
	if (flipCurrent) {
		flipCurrent.textContent = page;
	}
}

function prevPage() {
	if (currentIndex > 0) {
		showPage(currentIndex - 1);
	}
}

function nextPage() {
	if (currentIndex < totalPages - 1) {
		showPage(currentIndex + 1);
	}
}

// Slider Navigation
if (pageSlider) {
	pageSlider.addEventListener('input', (e) => {
		const page = parseInt(e.target.value);
		updateSidebar(page);

		if (currentMode === 'scroll') {
			const scrollView = document.getElementById('scroll-view');
			const images = scrollView.querySelectorAll('img');
			if (images[page - 1]) {
				images[page - 1].scrollIntoView({ behavior: 'auto', block: 'center' });
			}
		} else {
			showPage(page - 1);
		}
	});
}

// Scroll Observer
const observerOptions = {
	root: null,
	rootMargin: '-45% 0px -45% 0px', // Trigger when image crosses the middle 10% of screen
	threshold: 0
};

const observer = new IntersectionObserver((entries) => {
	if (currentMode !== 'scroll') return;

	entries.forEach(entry => {
		if (entry.isIntersecting) {
			// Find index of intersecting image
			const scrollView = document.getElementById('scroll-view');
			const images = Array.from(scrollView.querySelectorAll('img'));
			const index = images.indexOf(entry.target);

			if (index !== -1) {
				currentIndex = index;
				updateSidebar(currentIndex + 1);
			}
		}
	});
}, observerOptions);

// Initialize
document.addEventListener('DOMContentLoaded', () => {
	// Initialize Scroll Observer
	const scrollView = document.getElementById('scroll-view');
	const images = scrollView.querySelectorAll('img');
	images.forEach(img => observer.observe(img));

	// Initialize mode from URL
	const urlParams = new URLSearchParams(window.location.search);
	const mode = urlParams.get('mode');
	if (mode === 'flip') {
		setMode('flip');
	} else {
		// Initial sidebar update for scroll mode
		updateSidebar(1);
	}
});

// Keyboard navigation
document.addEventListener('keydown', (e) => {
	if (currentMode === 'flip') {
		if (e.key === 'ArrowLeft') prevPage();
		if (e.key === 'ArrowRight') nextPage();
	}
});
