// JavaScript for main interactions

// Function to handle form submission on booking page
function handleBookingFormSubmission(event) {
    // Prevent default form submission
    event.preventDefault();

    // Basic form validation example
    const checkInDate = document.getElementById("check_in").value;
    const checkOutDate = document.getElementById("check_out").value;
    
    if (new Date(checkInDate) >= new Date(checkOutDate)) {
        alert("Check-out date must be after the check-in date.");
        return;
    }

    // Additional validation checks can be added here

    // Submit form
    event.target.submit();
}

// Attach event listener to booking form (if exists)
const bookingForm = document.querySelector(".booking-form form");
if (bookingForm) {
    bookingForm.addEventListener("submit", handleBookingFormSubmission);
}

// Function to handle confirmation page printing
function printConfirmation() {
    window.print();
}

// Attach event listener to print button on confirmation page (if exists)
const printButton = document.querySelector(".confirmation a");
if (printButton) {
    printButton.addEventListener("click", printConfirmation);
}
