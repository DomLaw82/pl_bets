function showPopUp(popUpID, buttonID) {
	const popUp = document.getElementById(popUpID);
	const button = document.getElementById(buttonID);

	// Show the filter pop-up
	popUp.style.display = 'block';

	document.addEventListener('click', function(event) {
		// Check if the clicked element is outside the filter pop-up
		if (!popUp.contains(event.target) && !button.contains(event.target)) {
			// Hide the filter pop-up
			popUp.style.display = 'none';
		}
	});
}