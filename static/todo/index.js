const apiTodoAll = function(form, callback) {
    var path = '/api/todo/all'
    ajax('POST', path, '', callback)
}

const apiTodoAdd = function(form, callback) {
    let path = '/api/todo/add'
    ajax('POST', path, form, callback)
}

const apiTodoDelete = function(form, callback) {
    let path = '/api/todo/delete'
    ajax('POST', path, form, callback)
}

const bindTextdo = function(textValue) {
    let t = `
    <div class='mie-list mie-do'>
        <input class='fuck' type='checkbox'>
        <p class='pt'>${textValue}</p>
        <button class='disc' class='todelete'>丢弃</button>
    </div>`
    return t
}

const bindTextdone = function(textValue) {
    let t = `
    <div class='mie-list mie-done'>
        <input class='fuck' type='checkbox' checked='checked'>
        <p class='pt'>${textValue}</p>
        <button class='dele' class='todelete'>删除</button>
    </div>
    `
    return t
}

const listTextdele = function(textValue, classname) {
    let t = `
    <div class='mie-list mie-dele'>
        <span> </span>
        <p class='pt'>${textValue}</p>
        <button class='dele' class='todelete'>删除</button>
    </div>
    `
    return t
}

const addDo = function() {
    let form = {
        'state': todo,
    }
    apiTodoAll(form, function(r) {
        log(r)
    })
}

const main = function() {
    addDo()
}

main()
