<template>

  <PaginationTable
    tableTitle="Обучающиеся"
    tableWidth="98"
    :noTab="false"
    :addButton="false"
    :xlsxButton="true"
    getRecsURL="/backend/api/v1/guides/users/"
    :tableHeaders="tableHeaders"
    :fieldsArray="fieldsArray"
    :itemSelectEvent="userSelect"
  />

  <v-dialog
    persistent
    v-model="userDialog"
  >

    <ProfileForm
      v-if="userInfoTab === 'profile' && profileUuid.length > 0"
      :profileUuid="profileUuid"
      :closeDialogEvent="() => {userDialog = !(userDialog)}"
    />

  </v-dialog>

</template>

<script>
import PaginationTable from "@/components/tables/pagination_table/PaginationTable.vue";
import PaginationTableBaseField from "@/components/tables/pagination_table/PaginationTableBaseField.vue";
import ProfileForm from "@/components/forms/ProfileForm.vue";

export default {
  name: "StudentUsers",
  components: {ProfileForm, PaginationTableBaseField, PaginationTable},
  data() {
    return {
      tableHeaders: [
        {
          'title': 'Дата регистрации',
          'key': 'date_create'
        },
        {
          'title': 'Фамилия',
          'key': 'surname'
        },
        {
          'title': 'Имя',
          'key': 'name'
        },
        {
          'title': 'Отчество',
          'key': 'patronymic'
        },
        {
          'title': 'СНИЛС',
          'key': 'snils',
        },
        {
          'title': 'Телефон',
          'key': 'phone',
        },
        {
          'title': 'Email',
          'key': 'email',
        }
      ],
      fieldsArray: [
        {
          ui: 'date',
          key: 'date_create',
          addRequired: false,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'surname',
          addRequired: false,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'name',
          addRequired: false,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'patronymic',
          addRequired: false,
        },
        {
          ui: 'snils',
          key: 'snils',
          addRequired: false,
        },
        {
          ui: 'phone',
          key: 'phone',
          addRequired: false,
        },
        {
          ui: 'input',
          type: 'text',
          key: 'email',
          addRequired: false,
        }
      ],
      userDialog: false,
      profileUuid: '',
      userInfoTab: 'profile'
    }
  },
  methods: {
    userSelect(user) {
      this.userDialog = !(this.userDialog)
      this.profileUuid = user.object_id
      console.log(user.object_id)
    }
  }

}
</script>

<style scoped>

</style>
