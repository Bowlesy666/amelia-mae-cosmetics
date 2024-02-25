/**
 *  Show toast when user changes preferences
 * named this toast-cookie to eliminate issue of
 * django messages showing at the same time
 */
function showToastMessage(message, toastType) {
    var toastContainer = document.querySelector('.toast-container');

    toastContainer.innerHTML = '';

    // Create new
    var toastElement = document.createElement('div');
    toastElement.classList.add('toast-cookie');
    toastElement.classList.add('custom-toast');
    toastElement.classList.add('rounded-0');
    toastElement.classList.add('border-top-0');
    toastElement.setAttribute('data-autohide', 'false');
    var arrowUpElement = document.createElement('div');
    arrowUpElement.classList.add('arrow-up');
    arrowUpElement.classList.add('arrow-' + toastType);
    toastElement.appendChild(arrowUpElement);
    var toastCapperElement = document.createElement('div');
    toastCapperElement.classList.add('w-100');
    toastCapperElement.classList.add('toast-capper');
    toastCapperElement.classList.add('bg-' + toastType);
    toastElement.appendChild(toastCapperElement);

    // Create toast body
    var headerElement = document.createElement('div');
    headerElement.classList.add('toast-header');
    headerElement.classList.add('white-smoke');
    var titleElement = document.createElement('strong');
    titleElement.classList.add('mr-auto');
    titleElement.textContent = toastType.charAt(0).toUpperCase() + toastType.slice(1) + '!';
    var closeButton = document.createElement('button');
    closeButton.classList.add('ml-2');
    closeButton.classList.add('mb-1');
    closeButton.classList.add('close');
    closeButton.classList.add('text-dark');
    closeButton.setAttribute('data-dismiss', 'toast');
    closeButton.setAttribute('aria-label', 'Close');
    var closeIcon = document.createElement('span');
    closeIcon.setAttribute('aria-hidden', 'true');
    closeIcon.innerHTML = '&times;';
    closeButton.appendChild(closeIcon);
    headerElement.appendChild(titleElement);
    headerElement.appendChild(closeButton);
    toastElement.appendChild(headerElement);
    var bodyElement = document.createElement('div');
    bodyElement.classList.add('toast-body');
    bodyElement.classList.add('white-smoke');
    bodyElement.textContent = message;
    toastElement.appendChild(bodyElement);

    toastContainer.appendChild(toastElement);

    // Show toast-cookie
    $('.toast-cookie').toast('show');
}
