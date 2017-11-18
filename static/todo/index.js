const apiTodoAll = function(form, callback) {
    let path = '/api/todo/all?'
    for (let key in form) {
        if (form.hasOwnProperty(key)) {
            path += String(key) + '=' + String(form[key]) + '&'
        }
    }
    path = path.substring(0, path.length - 1)
    ajax('GET', path, '', callback)
}

const apiTodoAdd = function(form, callback) {
    let path = '/api/todo/add'
    ajax('POST', path, form, callback)
}

const apiTodoDelete = function(form, callback) {
    let path = '/api/todo/delete'
    ajax('POST', path, form, callback)
}

const apiTodoUpdate = function(form, callback) {
    let path = '/api/todo/update'
    ajax('POST', path, form, callback)
}

const bindTextdo = function(textValue, id) {
    let t = `
    <div class='mie-list mie-do' data-id=${id}>
        <input class='box-do' type='checkbox'>
        <p class='pt'>${textValue}</p>
        <button class='button-do'>丢弃</button>
    </div>`
    return t
}

const bindTextdone = function(textValue, id) {
    let t = `
    <div class='mie-list mie-done' data-id=${id}>
        <input class='box-done' type='checkbox' checked='checked'>
        <p class='pt'>${textValue}</p>
        <button class='button-done'>删除</button>
    </div>
    `
    return t
}

const bindTextdele = function(textValue, id) {
    let t = `
    <div class='mie-list mie-dele' data-id=${id}>
        <span> </span>
        <p class='pt'>${textValue}</p>
        <button class='button-delete'>删除</button>
    </div>
    `
    return t
}

const appendListEnd = function(text, id) {
    let t = e(id)
    t.insertAdjacentHTML('beforeEnd', text)
}

// 插入到正在进行后面
const appendTodoEnd = function(content, id) {
    let text = bindTextdo(content, id)
    scaler('#todo', '+')
    appendListEnd(text, '#list-todo')
}

// 插入到已完成后面
const appendDoneEnd = function(content, id) {
    let text = bindTextdone(content, id)
    scaler('#done', '+')
    appendListEnd(text, '#list-done')
}

// 插入到垃圾桶后面
const appendDeleEnd = function(content, id) {
    let text = bindTextdele(content, id)
    scaler('#dele', '+')
    appendListEnd(text, '#dele-list')
}

const allData = function(state, append) {
    let form = {
        'state': state,
    }
    apiTodoAll(form, function(r) {
        let data = JSON.parse(r)
        for (let i = 0; i < data.length; i++) {
            let content = data[i].content
            let id = data[i].id
            append(content, id)
        }
    })
}

const bindEventTodoList = function() {
    let addButton = e('#my-list')
    addButton.addEventListener('click', function(event) {
        let classname = event.target.className
        log(classname)
        functionTable(classname, event.target)
    })
}

const functionTable = function(classname, target) {
    let o = {}
    let model_ajax = function(target, state, append) {
        let p = target.parentElement
        let id = p.dataset.id
        let content = p.querySelector('.pt').textContent
        let form = {
            'id': id,
            'state': state,
        }
        apiTodoUpdate(form, function() {
            append(content, id)
            p.remove()
        })
    }

    o['box-do'] = function(target) {
        model_ajax(target, 'done', appendDoneEnd)
        scaler('#todo', '-')
    }

    o['box-done'] = function(target) {
        model_ajax(target, 'todo', appendTodoEnd)
        scaler('#done', '-')
    }

    o['button-do'] = function(target) {
        model_ajax(target, 'delete', appendDeleEnd)
        scaler('#todo', '-')
    }

    o['button-done'] = function(target) {
        model_ajax(target, 'delete', appendDeleEnd)
        scaler('#done', '-')
    }

    o['button-delete'] = function(target) {
        let p = target.parentElement
        let id = p.dataset.id
        let form = {
            'id': id,
        }
        apiTodoDelete(form, function() {
            p.remove()
            scaler('#dele', '-')
        })
    }

    return o[classname](target)
}

const buttonDisplay = function(id, disid) {
    let b = e(id)
    b.addEventListener('click', function(event) {
        let block_id = e(disid)
        let classlist = block_id.classList
        if (classlist.contains('mie-yin') == true) {
            classlist.remove('mie-yin')
        }
        else {
            classlist.add('mie-yin')
        }
    })
}

const scaler = function(id, op) {
    let t = e(id)
    let n = Number(t.innerText)
    if (op == '+') {
        t.innerText = n + 1
    }
    else {
        t.innerText = n - 1
    }
}

const addTodos = function() {
    allData('todo', appendTodoEnd)
    allData('done', appendDoneEnd)
    allData('delete', appendDeleEnd)
}

const addButtonDisplay = function() {
    buttonDisplay('#todo', '#list-todo')
    buttonDisplay('#done', '#list-done')
    buttonDisplay('#dele', '#dele-list')
}

const main = function() {
    addTodos()
    bindEventTodoList()
    addButtonDisplay()
}

main()
