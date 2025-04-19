import {notify} from "@kyvg/vue3-notification";

export function showAlert (type, title, text, noHide = false) {
    notify({type: type, title: title, text: text, duration: 5000})
}
