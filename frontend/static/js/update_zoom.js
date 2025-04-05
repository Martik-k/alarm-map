document.addEventListener('DOMContentLoaded', function() {
    const svgElement = document.querySelector('svg');
    const container = document.querySelector('body'); // Assuming the body is the container
    let zoomLevel = 1;
    let isDragging = false;
    let startX, startY, currentX = 0, currentY = 0;

    function applyTransform() {
        svgElement.style.transform = `scale(${zoomLevel}) translate(${currentX}px, ${currentY}px)`;
        svgElement.style.transformOrigin = 'center center'; // Keep zoom centered
    }

    function zoomIn() {
        zoomLevel += 0.1;
        applyTransform();
    }

    function zoomOut() {
        zoomLevel -= 0.1;
        if (zoomLevel <= 0.5) { // Set a minimum zoom level
            zoomLevel = 0.5;
        }
        applyTransform();
    }

    function startDrag(event) {
        isDragging = true;
        startX = event.clientX - currentX;
        startY = event.clientY - currentY;
        svgElement.style.transition = 'none'; // Disable transition during dragging for smoother movement
    }

    function drag(event) {
        if (isDragging) {
            let newX = event.clientX - startX;
            let newY = event.clientY - startY;

            // Calculate the boundaries
            const containerRect = container.getBoundingClientRect();
            const svgRect = svgElement.getBoundingClientRect();
            const minX = (containerRect.width - svgRect.width * zoomLevel) / 2;
            const maxX = (svgRect.width * zoomLevel - containerRect.width) / 2;
            const minY = (containerRect.height - svgRect.height * zoomLevel) / 2;
            const maxY = (svgRect.height * zoomLevel - containerRect.height) / 2;

            // Apply constraints
            newX = Math.max(minX, Math.min(newX, maxX));
            newY = Math.max(minY, Math.min(newY, maxY));

            currentX = newX;
            currentY = newY;
            applyTransform();
        }
    }

    function endDrag() {
        isDragging = false;
        svgElement.style.transition = 'transform 0.3s ease'; // Re-enable transition after dragging
    }

    svgElement.addEventListener('mousedown', startDrag);
    svgElement.addEventListener('mousemove', drag);
    svgElement.addEventListener('mouseup', endDrag);
    svgElement.addEventListener('mouseleave', endDrag);

    document.getElementById('zoom-in').addEventListener('click', zoomIn);
    document.getElementById('zoom-out').addEventListener('click', zoomOut);

    document.addEventListener('keydown', function(event) {
        if (event.ctrlKey && event.key === '+') {
            zoomIn();
        } else if (event.ctrlKey && event.key === '-') {
            zoomOut();
        }
    });
});