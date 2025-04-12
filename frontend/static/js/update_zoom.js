document.addEventListener('DOMContentLoaded', function() {
    const svgElement = document.querySelector('svg');
    const container = document.querySelector('body');
    let zoomLevel = 1;
    let isDragging = false;
    let startX, startY, currentX = 0, currentY = 0;
    
    function applyTransform() {
        if (!svgElement) return;
        svgElement.style.transform = `scale(${zoomLevel}) translate(${currentX / zoomLevel}px, ${currentY / zoomLevel}px)`;
        svgElement.style.transformOrigin = 'center center';
    }
    
    function zoomIn(event) {
        event?.preventDefault();
        zoomLevel *= 1.2; 
        applyTransform();
    }
    
    function zoomOut(event) {
        event?.preventDefault();
        zoomLevel /= 1.2;
        if (zoomLevel < 0.1) {
            zoomLevel = 0.1; 
        }
        applyTransform();
    }
    
    function handleWheel(event) {
        event.preventDefault();
        if (event.deltaY < 0) {
            zoomIn();
        } else {
            zoomOut();
        }
    }
    
    function startDrag(event) {
        if (!svgElement) return;
        if (event.button !== 0) return;
        isDragging = true;
        startX = event.clientX - currentX;
        startY = event.clientY - currentY;
        svgElement.style.cursor = 'grabbing';
        svgElement.style.transition = 'none';
    }
    
    function drag(event) {
        if (!isDragging || !svgElement) return;
        currentX = event.clientX - startX;
        currentY = event.clientY - startY;
        applyTransform();
    }
    
    function endDrag() {
        if (!svgElement) return;
        isDragging = false;
        svgElement.style.cursor = 'grab';
        svgElement.style.transition = 'transform 0.1s ease';
    }
    
   
    if (svgElement) {
        svgElement.style.cursor = 'grab';
        svgElement.addEventListener('mousedown', startDrag);
        document.addEventListener('mousemove', drag);
        document.addEventListener('mouseup', endDrag);
        svgElement.addEventListener('wheel', handleWheel, { passive: false });
    }
    

    document.getElementById('zoom-in')?.addEventListener('click', zoomIn);
    document.getElementById('zoom-out')?.addEventListener('click', zoomOut);
   
    document.addEventListener('keydown', function(event) {
        if (event.ctrlKey) {
            if (event.key === '+' || event.key === '=') {
                event.preventDefault();
                zoomIn();
            } else if (event.key === '-') {
                event.preventDefault();
                zoomOut();
            }
        }
    });
});