function generateList(containerID, elemetsList, eventFunction){
    elemetsList.forEach(element => {
        const itemElement = document.createElement('div');
        itemElement.textContent = element;
        containerID.appendChild(itemElement);
        console.log(itemElement)
        itemElement.addEventListener('click', () => eventFunction(itemElement));
    });
}

function _selectOneScrollableListItem(containerID, itemElement){
    const allItems = containerID.querySelectorAll('div');
    allItems.forEach(el => el.classList.remove('selected'));

    itemElement.classList.add('selected');
}

function _selectMultipleListItems(itemElement){
    if (itemElement.classList.contains('selected')){
        itemElement.classList.remove('selected')
    } else {
        itemElement.classList.add('selected');
    }
}

function clearList(containerID){
    while (containerID.firstChild) {
        containerID.removeChild(containerID.firstChild);
    }
}