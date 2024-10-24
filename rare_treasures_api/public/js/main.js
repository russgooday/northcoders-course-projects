// Description: Main JS file for the Rare Treasures API

// Wrap the text of an element in a span with a given class
function wrapWithSpan(className = '') {
    function wrapElement(el) {
        el.innerHTML = `<span class=${className}>${el.textContent}</span>`
        return el
    }

    return wrapElement
}

// Set a CSS variable on an element e.g. ('--width', '100px')
function setVariable(prop, value) {
    function setElementVar(el) {
        el.style.setProperty(prop, value)
        return el
    }
    return setElementVar
}

// Get the maximum width of the first child of each element in the list
function getMaxWidth(els) {
    let maxWidth = 0
    for (const el of els) {
        const { width } = el.firstChild.getBoundingClientRect()
        if (width > maxWidth) maxWidth = width;
    }
    return maxWidth
}

// wrap text in spans and set the width variable to the maximum width
function justifyRight(els) {
    els.forEach(wrapWithSpan('align-right'))
    const maxWidth = getMaxWidth(els) + 'px'
    els.forEach(setVariable('--width', maxWidth))

    return els
}

// Align the columns of a table
// Args: the column numbers to align
function alignColumns(...num) {
    const table = document.querySelector('#treasures_table table')
    if (!table) return

    for (const n of num) {
        table.querySelector(`th:nth-child(${n})`).classList.add('align-center')
        justifyRight(table.querySelectorAll(`td:nth-child(${n})`))
    }
}

export { alignColumns }
