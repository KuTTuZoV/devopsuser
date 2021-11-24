const services = document.querySelector('#services')
const form = document.querySelector('form')
form.addEventListener('submit', ev => {
    ev.preventDefault()
    const url = form.action
    const formData = new FormData(form)
    fetch(url, {method:'post', body:formData})
        .then(res => {
            switch(res.status){
                case 200:
                    return Promise.resolve()
                default:
                    return Promise.reject()
            }
        })
        .then($ => {
            alert('Сервис зарегистрирован успешно')
            showServices()
            form.reset()
        })
        .catch($ => alert('Во время регистрации произошла ошибка'))
})

function showServices(){
    services.innerHTML = ''
    fetch('/api/service')
        .then(res => res.text())
        .then(txt => {
            const lines = txt.trim().split('\n')
            lines.forEach(line => {
                const service = document.createElement('span')
                service.setAttribute('class', 'badge rounded-pill bg-primary badge-with-margin')
                service.textContent = line
                services.appendChild(service)
            })
        })
}

showServices()
