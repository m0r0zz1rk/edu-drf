import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import {createVuetify} from "vuetify";
import { VDateInput } from 'vuetify/labs/VDateInput'
import {createI18n, useI18n} from "vue-i18n";
import {createVueI18nAdapter} from "vuetify/locale/adapters/vue-i18n";
import {ru} from "vuetify/locale";
import {VNumberInput} from "vuetify/labs/components";

const cokoTheme = {
  dark: false,
  colors: {
    'coko-blue': '#373c59',
    'coko-red': '#FF5722'
  }
}

const messages = {
  ru: {
    $vuetify: {
      ...ru,
      dataIterator: {
        rowsPerPageText: 'Items per page:',
        pageText: '{0}-{1} of {2}',
      },
      confirmEdit: {
        cancel: 'Отмена',
        ok: 'OK'
      }
    },
  },
}

const i18n = createI18n({
  legacy: false, // Vuetify does not support the legacy mode of vue-i18n
  locale: 'ru',
  fallbackLocale: 'ru',
  messages
})


export const vuetify = createVuetify({
  locale: {
    adapter: createVueI18nAdapter({ i18n, useI18n }),
  },
  components: {
    VDateInput,
    VNumberInput,
  },
  theme: {
    defaultTheme: 'cokoTheme',
    themes: {
      cokoTheme
    }
  }
})
