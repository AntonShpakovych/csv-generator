function SchemaNewColumn() {
    const addColumn = document.getElementById("schema-add-column");
    const columnFormsDiv = document.getElementById("column-forms");
    const regex = new RegExp("__prefix__", "g");
    const totalNewForms = document.getElementById(
    "id_columns-TOTAL_FORMS"
    );

    function cloneAndModifyForm() {
        const quantityOfColumnForm = columnFormsDiv.getElementsByClassName("column-form").length
        const schemaEmptyColumnForm = document.getElementById("empty-column-form-clone");
        const divForClone = schemaEmptyColumnForm.getElementsByClassName("column-form")
        const newForm = divForClone[divForClone.length - 1].cloneNode(true);

        newForm.innerHTML = newForm.innerHTML.replace(regex, quantityOfColumnForm);
        columnFormsDiv.append(newForm)
        totalNewForms.setAttribute("value", quantityOfColumnForm + 1)
    }

    addColumn.addEventListener("click", cloneAndModifyForm);
}


window.addEventListener("load", function() {
    const create_path = "/schemas/create/"
    const update_path = /^\/schemas\/(\d+)\/update\/$/

    if (window.location.pathname === create_path || window.location.pathname.match(update_path)) {
        SchemaNewColumn()
    }
});
