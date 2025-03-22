import {notify} from "@kyvg/vue3-notification";

export function showAlert (type, title, text, noHide = false) {
    // Отобразить v-alert с полученным типом и текстом (параметр отображения без автоматического закрытия - по ситуации)
    // if (['success', 'warning', 'info', 'error'].includes(type)) {
    //     try {
    //         let alert = document.querySelector('#'+type+'-alert')
    //         if (!(alert.classList.contains('alert-visible'))) {
    //             alert.classList.remove('alert-hidden')
    //             alert.classList.add('alert-visible')
    //             let vAlertContent = alert.querySelector('.v-alert__content')
    //             vAlertContent.innerHTML=`
    //               <div class='v-alert-title'>`+title+`</div>`+text
    //             if (!(noHide)) {
    //                 setTimeout(() => hideAlert(type), 4000)
    //             }
    //         }
    //     } catch (e) {
    //         console.log(e)
    //     }
    //
    // }
    notify({type: type, title: title, text: text, duration: 5000})
}

export function hideAlert(type) {
    // Скрыть v-alert полученного типа
    try {
        let alert = document.querySelector('#'+type+'-alert')
        if (alert.classList.contains('alert-visible')) {
            alert.classList.remove('alert-visible')
            alert.classList.add('alert-hidden')
        }
    } catch (e) {
        console.log(e)
    }
}
