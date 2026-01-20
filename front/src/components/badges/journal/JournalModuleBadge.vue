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
          alias: 'ЦОКО'
        },
        {
          name: 'APPLICATIONS',
          alias: 'Заявки'
        },
        {
          name: 'AUTHEN',
          alias: 'Авторизация'
        },
        {
          name: 'CELERY',
          alias: 'Celery'
        },
        {
          name: 'DOCS',
          alias: 'Документы'
        },
        {
          name: 'EDU',
          alias: 'Учебная часть'
        },
        {
          name: 'GUIDES',
          alias: 'Справочники'
        },
        {
          name: 'JOURNAL',
          alias: 'Журнал событий'
        },
        {
          name: 'REPORTS',
          alias: 'Отчеты'
        },
        {
          name: 'SETTINGS',
          alias: 'Настройки'
        },
        {
          name: 'SURVEYS',
          alias: 'Опросы'
        },
        {
          name: 'USERS',
          alias: 'Обучающийся'
        },
        {
          name: 'ORM',
          alias: 'Работа с БД'
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
