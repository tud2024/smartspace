/* Breadcrumb Java script */

document.addEventListener("DOMContentLoaded", function () {
    const breadcrumbsContainer = document.querySelector(".breadcrumb");
    const pathArray = window.location.pathname.split("/").filter(segment => segment);

    let breadcrumbHTML = `<li class="breadcrumb-item"><a href="/">Home</a></li>`;
    let path = "";

    pathArray.forEach((segment, index) => {
        path += `/${segment}`;
        if (index === pathArray.length - 1) {
            breadcrumbHTML += `<li class="breadcrumb-item active" aria-current="page">${decodeURIComponent(segment)}</li>`;
        } else {
            breadcrumbHTML += `<li class="breadcrumb-item"><a href="${path}">${decodeURIComponent(segment)}</a></li>`;
        }
    });

    breadcrumbsContainer.innerHTML = breadcrumbHTML;
});
