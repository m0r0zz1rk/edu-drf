<template>
  <v-badge
    color="info"
    :content="displayAlias"
    inline
  ></v-badge>
</template>

<script>
export default {
  name: "JournalModuleBadge",
  props: {
    moduleName: String, // Полученное имя модуля
  },
  data() {
    return {
      displayAlias: '',
      modules: [
        {
          name: 'COMMON',
          alias: 'Общий'
        },
        {
          name: 'ADMINS',
          alias: 'ЛК администратора'
        },
        {
          name: 'APPLICATIONS',
          alias: 'Модуль заявок'
        },
        {
          name: 'AUTHEN',
          alias: 'Модуль авторизации/регистрации'
        },
        {
          name: 'CELERY',
          alias: 'Модуль очереди задач Celery'
        },
        {
          name: 'DOCS',
          alias: 'Модуль документов'
        },
        {
          name: 'EDU',
          alias: 'Модуль учебной части'
        },
        {
          name: 'GUIDES',
          alias: 'Модуль справочников'
        },
        {
          name: 'JOURNAL',
          alias: 'Модуль журнала событий'
        },
        {
          name: 'REPORTS',
          alias: 'Модуль отчетов'
        },
        {
          name: 'SETTINGS',
          alias: 'Модуль настроек'
        },
        {
          name: 'SURVEYS',
          alias: 'Модуль опросов'
        },
        {
          name: 'USERS',
          alias: 'ЛК Пользователя'
        }
      ]
    }
  },
  mounted() {
    this.modules.map((module) => {
      if (module.name === this.moduleName) {
        this.displayAlias = module.alias
        return false
      }
    })
  }
}
</script>

<style scoped>

</style>
