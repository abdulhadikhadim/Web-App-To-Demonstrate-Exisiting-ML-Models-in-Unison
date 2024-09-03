document.addEventListener('DOMContentLoaded', function () {
    // Initialize Bootstrap tab functionality
    var triggerTabList = [].slice.call(document.querySelectorAll('.btn-group .btn'))
    triggerTabList.forEach(function (triggerEl) {
        var tabTrigger = new bootstrap.Tab(triggerEl)

        triggerEl.addEventListener('click', function (event) {
            event.preventDefault()
            tabTrigger.show()
        })
    })

    // Ensure the correct tab is active on page load
    const activeTab = document.querySelector('.btn-group .btn.active');
    if (activeTab) {
        const activeContentId = activeTab.getAttribute('data-bs-target');
        const activeContent = document.querySelector(activeContentId);
        activeContent.classList.add('show', 'active');
    }
});
