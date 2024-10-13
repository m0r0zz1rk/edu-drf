<template>

  <LkPage :usePreLoader="usePreLoader">
    <slot>
      <v-card
          color="coko-blue"
          class="lk-full-page-card"
          title="Мероприятия (ИКУ)"
      >
        <v-card-text>
          <div

          >

            <template
                style="text-align: center"
                v-if="!events"
            >
              <b>Пожалуйста подождите...</b>
            </template>

            <template
                v-if="events"
            >

              <v-expansion-panels
                  style="padding-top: 5px"
                  v-model="departmentsPanels"
                  color="coko-blue"
                  multiple
              >

                <v-expansion-panel
                    v-for="dep in events"
                >

                  <v-expansion-panel-title
                      color="coko-blue"
                  >
                    <div style="font-size: 18px">
                      {{dep.department}}
                    </div>
                  </v-expansion-panel-title>

                  <v-expansion-panel-text>

                    <v-row
                        dense
                    >

                      <v-col
                          v-for="event in dep.services"
                          cols="12"
                          md="3"
                          sm="6"
                      >

                        <v-card
                            color="coko-blue"
                            @click="openEventDetailDialog(event, dep.department)"
                            variant="tonal"
                        >
                          <v-card-title>
                            <div style="text-align: center">
                              {{event.code}}
                            </div>

                          </v-card-title>

                          <v-card-text
                              class="internal-card-text"
                          >
                            <div
                                style="color: black; text-align: center;"
                            >

                              <b>{{event.title}}</b>
                              <br/><br/>
                              Сроки обучения:<br/>
                              <b>{{event.date_start}}-{{event.date_end}}</b>
                              <br/>
                              Куратор:<br/>
                              <b>{{event.curator_fio}}</b>

                            </div>

                          </v-card-text>
                        </v-card>

                      </v-col>
                    </v-row>

                  </v-expansion-panel-text>

                </v-expansion-panel>

              </v-expansion-panels>

            </template>

          </div>
        </v-card-text>

        <v-spacer></v-spacer>

      </v-card>
    </slot>
  </LkPage>

  <ServiceDetail
      ref="eventDetail"
      serviceType="event"
      :serviceInfo="selectedEvent"
      :department="eventDep"
  />

</template>

<script>

// Страница для просмотра списка доступных для регистрации мероприятий
import LkPage from "@/components/LkPage.vue";
import ServiceDetail from "@/components/dialogs/students/service/ServiceDetail.vue";
import {apiRequest} from "@/commons/api_request";
import {showAlert} from "@/commons/alerts";

export default {
  name: 'Events',
  components: {ServiceDetail, LkPage},
  props: {
    // Функция для отображения/скрытия анимации загрузки на странице
    usePreLoader: Function,
  },
  data() {
    return {
      // Параметр отображения загрузки на элементах формы
      loading: true,
      // Список мероприятий, сгруппированных по подразделениям
      events: null,
      // Список открытых панелей с курсами департаментов
      departmentsPanels: [],
      // Выбранное мероприятие
      selectedEvent: null,
      // Подразделение выбранного мероприятия
      eventDep: ''
    }
  },
  methods: {
    // Открыть диалоговое окно с детальной инфомрацией по мероприятию
    openEventDetailDialog(course, dep) {
      this.selectedEvent = course
      this.eventDep = dep
      this.$refs.eventDetail.openDialog()

    },
    // Получение мероприятий, сгруппированных по подразделениям
    async getEvents() {
      let eventsRequest = await apiRequest(
          '/backend/api/v1/users/events/',
          'GET',
          true,
          null
      )
      if (eventsRequest.error) {
        showAlert(
            'error',
            'Мероприятия',
            eventsRequest.error
        )
      } else {
        this.events = eventsRequest.success
        for (let i=0;i<this.events.length;i++) {
          this.departmentsPanels.push(i)
        }
        eventsRequest.success.map((dep) => {
          this.departmentsPanels.push(dep.department)
        })
      }
      this.loading = false
    }
  },
  mounted() {
    this.getEvents()
  }
}

</script>

<style scoped>

</style>