// Статусы заявок обучающихся
const appStatuses = [
    {
        key: 'draft',
        title: 'Черновик',
        color: 'yellow'
    },
    {
        key: 'work',
        title: 'В работе',
        color: 'red'
    },
    {
        key: 'wait_pay',
        title: 'Ждем оплаты',
        color: 'purple'
    },
    {
        key: 'check',
        title: 'На проверке',
        color: 'blue'
    },
    {
        key: 'pay',
        title: 'Оплачено',
        color: 'light-green'
    },
    {
        key: 'study',
        title: 'Проходит обучение',
        color: 'green'
    },
    {
        key: 'study_complete',
        title: 'Обучение завершено',
        color: 'grey'
    },
    {
        key: 'archive',
        title: 'Архив',
        color: 'black'
    },
]

export default appStatuses