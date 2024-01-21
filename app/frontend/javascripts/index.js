function showPopUp(popUpID, buttonID) {
	const popUpBackground = document.getElementById('pop-up-background');
	const popUp = document.getElementById(popUpID);
	const button = document.getElementById(buttonID);

	// Show the filter pop-up
	popUp.style.display = 'block';
	popUpBackground.style.display = 'block';

	document.addEventListener('click', function(event) {
		// Check if the clicked element is outside the filter pop-up
		if (event.target.id == 'pop-up-background') {
			// Hide the filter pop-up
			popUp.style.display = 'none';
			popUpBackground.style.display = 'none';
		}
	});
}

//BUG - On matches page, after add-results popup is dismissed, using the filter popup results in the overlay not showing, but the filter popup still works