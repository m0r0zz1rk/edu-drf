<script setup>
import {ref, watch} from 'vue'
import CokoDialog from "@/components/dialogs/CokoDialog.vue";
import {showAlert} from "@/commons/alerts";

// Функции установки параметров согласия на отправку по Email и согласия на отправку по номеру телефона
const {
  emailMailing,
  phoneMailing,
  setMailingByEmail,
  setMailingByPhone,
  showMainButton,
  onMailingClose
} = defineProps({
  emailMailing: Boolean | null,
  phoneMailing: Boolean | null,
  setMailingByEmail: Function,
  setMailingByPhone: Function,
  showMainButton: Boolean,
  onMailingClose: Function,
})

// Параметр блокировки кнопок
const loading = ref(false)

// Ссылка на диалоговое окно с согласием на получение рассылки
const innerMailingDialog = ref(null)
// Хэндлер для открытия диалогового окна с согласием на рассылку
const openMailingDialog = () => {innerMailingDialog.value.dialog = true}
// Хэндлер для закрытия диалогового окна с согласием на рассылку
const closeMailingDialog = () => {
  loading.value = true
  setTimeout(() => {
    if (onMailingClose) {
      onMailingClose()
    }
    loading.value = false
    innerMailingDialog.value.dialog = false
  }, 1000)
}

// Ссылка на диалоговое окно с согласием на обработку ПДн при получении рассылки
const innerPDnDialog = ref(null)
// Хэндлер для открытия диалогового окна с согласием на обработку ПДн
const openPDnDialog = () => {innerPDnDialog.value.dialog = true}
// Хэндлер для закрытия диалогового окна с согласием на обработку ПДн
const closePDnDialog = () => {innerPDnDialog.value.dialog = false}

// Цвет обводки чекбоксов и текста
const infoColor = ref('black')
// Установка дефолтного цвета
const setDefaultInfoColor = () => {infoColor.value = 'black'}

// Согласие на отправку информации по Email
const mailingByEmail = ref(emailMailing !== null ? emailMailing : true)
watch(mailingByEmail, (newVal, oldVal) => {setMailingByEmail(newVal)})

// Согласие на отправку информации по телефону
const mailingByPhone = ref(phoneMailing !== null ? phoneMailing : true)
watch(mailingByPhone, (newVal, oldVal) => {setMailingByPhone(newVal)})


// Хэндлер при нажатии на кнопку отказа от рассылки
const handleNotAgreedMailing = () => {
  setDefaultInfoColor()
  if (confirm('Вы уверены, что не даете свое согласие на получение рассылки?')) {
    mailingByPhone.value = false
    mailingByEmail.value = false
    closeMailingDialog()
  }
}

// Хэндлер при нажатии на кнопку согласия на рассылки
const handleAgreedMailing = () => {
  setDefaultInfoColor()
  if (!mailingByEmail.value && !mailingByPhone.value) {
    infoColor.value = 'red'
    showAlert('error', 'Способы рассылки', 'Выберите способы рассылки')
    return false
  }
  openPDnDialog()
}

// Хэндлер при нажатии на кнопку отказа от обработки ПДн
const handleNotAgreedPDn = () => {
  alert('В таком случае Вы не сможете получать информацию о предстоящих курсах и семинарах ' +
      'выбранным Вами способом направления рассылки')
  closePDnDialog()
}

// Хэндлер при нажатии на кнопку согласия на обработку ПДн
const handleAgreedPDn = () => {
  closePDnDialog()
  closeMailingDialog()
}

defineExpose({openMailingDialog})

</script>

<template>
  <v-btn v-if="showMainButton" text="Согласие на получение рассылки" color="coko-blue" @click="openMailingDialog"/>

  <CokoDialog ref="innerMailingDialog" :cardActions="true" :hideCloseButton="true">
    <template v-slot:title>
      Согласие на получение рассылки
    </template>

    <template v-slot:text>
      <p>
        <i style="font-size: 12px">Внимательно ознакомьтесь с текстом настоящего Согласия, после чего примите
          решение о предоставлении или в отказе в предоставлении ГАУ ИО «Центр оценки профессионального мастерства,
          квалификаций педагогов и мониторинга качества образования» согласия <b>на рассылку Вам информации о
          предстоящих курсах и семинарах (далее – информационная рассылка)</b>. Согласием с Вашей стороны на получение
          информационных рассылок будет являться нажатие на кнопку «Даю согласие» в разделе «Я даю согласие на
          получение информационных рассылок» (согласие путём конклюдентных действий).</i><br/><br/>
        Путём конклюдентных действий (нажимая на кнопку «Даю согласие»), свободно, своей волей и в своем
        интересе даю согласие ГАУ ИО «Центр оценки профессионального мастерства, квалификаций педагогов и
        мониторинга качества образования» (ИНН 3811469215 КПП 381101001 ОГРН 1203800010150, юридический: 664023,
        Иркутская область, г. Иркутск, ул. Лыткина, стр. 75/1 (далее – Оператор), на направление мне и получение
        мной информационных рассылок на следующих условиях:<br/>
        <v-checkbox
            :color="infoColor"
            v-model="mailingByPhone"
        >
          <template v-slot:label>
            <p :style="`color: ${infoColor}`">посредством мессенджеров и СМС сообщений с использованием
              моего номера телефона, указанного в личном кабинете</p>
          </template>
        </v-checkbox>
        <v-checkbox
            :color="infoColor"
            v-model="mailingByEmail"
            style="margin-top: -25px"
        >
          <template v-slot:label>
            <p :style="`color: ${infoColor}`">на мою электронную почту, указанную в личном кабинете</p>
          </template>
        </v-checkbox>
        <b>Я гарантирую, что:</b><br/>
        указанные мной номер мобильного телефона и адрес электронной почты принадлежат мне,
        соответственно получать информационные рассылки буду я.
        За достоверность предоставленных данных ответственность беру на себя;<br/>
        в случае прекращения использования номера мобильного телефона и/или адреса электронной почты,
        проинформирую об этом Оператора.<br/><br/>
        <b>Настоящее Согласие действует бессрочно и может быть отозвано в любое время по моему письменному заявлению.</b><br/>
        Я проинформирован(а), что кнопка отказа от рассылок расположена в моем личном кабинете в разделе «Профиль».<br/>
        Подтверждаю, что настоящее Согласие является достаточной формой согласия для направления мне информационных рассылок.
      </p>
    </template>

    <template v-slot:actions>
      <v-spacer/>
      <v-btn :loading="loading" color="coko-blue" variant="flat" @click="handleNotAgreedMailing" text="НЕ даю согласие" />
      <v-btn :loading="loading" color="coko-blue" variant="flat" @click="handleAgreedMailing" text="Даю согласие" />
    </template>

  </CokoDialog>

  <CokoDialog ref="innerPDnDialog" :cardActions="true" :hideCloseButton="true">

    <template v-slot:title>Согласие на обработку персональных данных при получении рассылки</template>

    <template v-slot:text>
      <p>
        Нажимая кнопку «Даю согласие» я даю свое согласие Государственному автономному учреждению Иркутской
        области «Центр оценки профессионального мастерства, квалификаций педагогов и мониторинга качества
        образования» (далее - ГАУ ИО ЦОПМКиМКО), адрес местонахождения: 664023, Иркутская область, город
        Иркутск, улица Лыткина, строение 75/1, на осуществление автоматизированной обработки персональных
        данных, включая сбор, систематизацию, накопление, хранение, уточнение (обновление, изменение),
        использование, уничтожение для осуществления действий по направлению мне информационных рассылок
        <em>с целью</em> информирования меня о предстоящих курсах и семинарах в ГАУ ИО ЦОПМКиМКО.<br/>
        <b>Согласие дается для обработки следующих персональных данных:</b><br/>
        - фамилия, имя, отчество (при наличии);<br/>
        - адрес электронной почты;<br/>
        - номер мобильного телефона.<br/>
        Настоящее согласие дано мной добровольно и действует с момента его подписания до отзыва моего 
        согласия на получение рассылок о предстоящих курсах и семинарах.<br/>
        Я уведомлен(а), что вправе отозвать настоящее согласие, выданное мной ГАУ ИО ЦОПМКиМКО путем 
        отказа от рассылки о предстоящих курсах и семинарах.<br/>
        Я подтверждаю, что, давая такое согласие, я действую по собственной воле и в своих интересах.
      </p>
    </template>
    
    <template v-slot:actions>
      <v-spacer/>
      <v-btn color="coko-blue" variant="flat" @click="handleNotAgreedPDn">Не даю согласие</v-btn>
      <v-btn color="coko-blue" variant="flat" @click="handleAgreedPDn">Даю согласие</v-btn>
    </template>

  </CokoDialog>

</template>

<style scoped>

</style>