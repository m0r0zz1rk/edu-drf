<template>
  <div v-if="showField">

    <v-text-field
      v-if="field.ui === 'input'"
      :type="field.type"
      :v-mask="
        ['phone', 'snils'].includes(field.ui) &&
          field.ui === 'snils' ?
            '###-###-### ##'
            :
            '+7 (###) ###-##-##'
      "
      v-model="localValue"
      :label="fieldTitle ?
                !checkRequired ?
                  fieldTitle
                  :
                  field.addRequired ?
                    fieldTitle+'*'
                    :
                    fieldTitle
              :
              ''
      "
      @change="e => onChangeEvent(field.key, localValue)"
    />

    <v-text-field
      v-if="field.ui === 'phone'"
      v-mask="'+7 (###) ###-##-##'"
      v-model="localValue"
      :label="fieldTitle ?
                !checkRequired ?
                  fieldTitle
                  :
                  field.addRequired ?
                    fieldTitle+'*'
                    :
                    fieldTitle
              :
              ''
      "
      @change="e => onChangeEvent(field.key, localValue)"
    />

    <v-text-field
      v-if="field.ui === 'snils'"
      v-mask="'###-###-### ##'"
      v-model="localValue"
      :label="fieldTitle ?
                !checkRequired ?
                  fieldTitle
                  :
                  field.addRequired ?
                    fieldTitle+'*'
                    :
                    fieldTitle
              :
              ''
      "
      @change="e => onChangeEvent(field.key, localValue)"
    />

    <v-select
      v-if="['select', 'journalModule', 'journalRecStatus'].includes(field.ui)"
      :items="[
        '',
        ...field.items
      ]"
      v-model="localValue"
      :label="fieldTitle ?
                !checkRequired ?
                  fieldTitle
                  :
                  field.addRequired ?
                    fieldTitle+'*'
                    :
                    fieldTitle
              :
              ''
      "
      @update:modelValue="e => onChangeEvent(field.key, localValue)"
    />

    <v-date-input
      v-if="field.ui === 'date'"
      v-model="localValue"
      :label="fieldTitle ?
                !checkRequired ?
                  fieldTitle
                  :
                  field.addRequired ?
                    fieldTitle+'*'
                    :
                    fieldTitle
              :
              ''
      "
      prepend-icon=""
      prepend-inner-icon="$calendar"
      @update:modelValue="e => {
        if (onChangeEvent) {
          onChangeEvent(field.key, convertDateToBackend(this.localValue))
        }
      }"
      @click:clear="e => {this.localValue = null; onChangeEvent(field.key, '')}"
      clearable
    ></v-date-input>
  </div>
</template>

<script>
import {convertDateToBackend} from "@/commons/date";

export default {
  name: "PaginationTableBaseField",
  props: {
    useInTableManage: Boolean, // Параметр вызова компонента из PaginationTableManage
    checkRequired: Boolean, // Параметр, отображющий необходимость проверки обязательного заполнения
    field: Object, // Объекта fieldsArray
    value: String, // Значение (при редактировании записи)
    fieldTitle: String, // Наименование поля
    onChangeEvent: Function, //Функция, вызываемая при изменении
  },
  data() {
    return {
      localValue: '',
      showField: false,
    }
  },
  methods: {
    convertDateToBackend,
    checkUiDate() {
      if (this.field.ui === 'date') {
        this.localValue = null
      }
    },
  },
  mounted() {
    if (this.value) {
        this.localValue = this.value
    }
    if (this.useInTableManage) {
        this.showField = this.useInTableManage
    }
    this.checkUiDate()
  }
}
</script>

<style scoped>

</style>
