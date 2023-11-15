function schemaDeleteColumn(checkbox) {
    const parentDiv = checkbox.closest(".column-form")

    if (checkbox.checked) {
        parentDiv.style.display = "none"
    } else {
        parentDiv.style.display = "block"
    }
}
