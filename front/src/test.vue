<template>
  <Header />

  <div v-if="downloadLoad">
    <div id="main-content">
      <b>Подождите, выполняется формирование файла...</b>
    </div><br>
    <div id="main-content">
      <img src="../../../../assets/gifs/load.gif">
    </div>
  </div>

  <div v-if="!(downloadLoad)">

    <TablesGrid>

      <template v-slot:grid-menu-nav>
        <router-link class="nav-href" to="/centre/guides">
          <div style="display: inline;">
            <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                    type="button">
              <font-awesome-icon icon="fa-solid fa-database" :style="{ color: white }"/>
            </button>
          </div>
        </router-link>&nbsp;
        <router-link class="nav-href" to="">
          <div style="display: inline;">
            <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                    type="button" disabled>
              <font-awesome-icon icon="fa-solid fa-chart-line" :style="{ color: white }"/>
            </button>
          </div>
        </router-link>&nbsp;
        <router-link class="nav-href" to="">
          <div style="display: inline;">
            <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                    type="button" disabled>
              <font-awesome-icon icon="fa-solid fa-newspaper" :style="{ color: white }"/>
            </button>
          </div>
        </router-link>&nbsp;

      </template>

      <template v-slot:table-grid-name>
        <table style="width: 65vw;">
          <tr>
            <td style="width: 90%">
              Таблица "14 видов работ по ФП"
              (<a href="#" @click="showModalAction('tables')">Сменить таблицу</a>)
            </td>
            <td style="width: 10%">
              <button class="btn btn-lg btn-primary iohk-butt" @click="openSideBox('period')">Периоды</button>
            </td>
          </tr>
        </table>
      </template>

      <template v-slot:grid-control-buttons>
        <a href="#" @click ="openSideBox('add')">
          <div style="display: inline;">
            <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                    type="button">
              <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>
            </button>
          </div>
        </a>&nbsp;
        <a href="#" @click = "openSideBox('find')">
          <div style="display: inline;">
            <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                    type="button">
              <font-awesome-icon icon="fa-solid fa-magnifying-glass" :style="{ color: white }"/>
            </button>
          </div>
        </a>&nbsp;
        <a href="#" @click = "downloadExcel();">
          <div style="display: inline;">
            <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                    type="button">
              <font-awesome-icon icon="fa-solid fa-file-excel" :style="{ color: white }"/>
            </button>
          </div>
        </a>
      </template>

      <template v-slot:table-grid-info>

        <div id="main-content">

          <div v-bind:class="[LoadClass]">
            <img src="../../../../assets/gifs/load.gif">
          </div>

        </div>

        <div v-bind:class="[ContentClass]">
          <div class="container-table">
            <div class="table-wrapper">
              <form @submit.prevent="newPurchase();">
                <table class="fl-table mini-font" style="width: 170vw;">
                  <thead >
                  <tr>
                    <th rowspan="2">№</th>
                    <th v-if="selectPeriod == 'Все'" rowspan="2">
                      Год<br>н.р.
                    </th>
                    <th v-if="selectPeriod == 'Все'" rowspan="2">
                      Год<br>о.р.
                    </th>
                    <th rowspan="2">МО</th>
                    <th rowspan="2">Должностное лицо (ФИО, должность, телефон)</th>
                    <th rowspan="2">Контактное лицо (ФИО, телефон)</th>
                    <th rowspan="2">Объект</th>
                    <th rowspan="2">Дата и номер соглашения м/у министерством образования ИО и МО</th>
                    <th rowspan="2">Мероприятие <font-awesome-icon icon="fa-solid fa-filter"
                                                                   @click="openFilter('event_name')"
                                                                   :style="{ color: white }"/></th>
                    <th colspan="2" style="width:10%;">Размер субсидий на мероприятие, рублей</th>
                    <th rowspan="2">Дата объявления закупки <font-awesome-icon icon="fa-solid fa-filter"
                                                                               @click="openFilter('date_announce')"
                                                                               :style="{ color: white }"/></th>
                    <th rowspan="2" style="width:10%;">Ссылка на закупку </th>
                    <th rowspan="2">Дата проведения аукциона <font-awesome-icon icon="fa-solid fa-filter"
                                                                                @click="openFilter('date_auction')"
                                                                                :style="{ color: white }"/></th>
                    <th rowspan="2" style="width:10%;">Подрядчик/Поставщик, дата, номер контракта <font-awesome-icon icon="fa-solid fa-filter"
                                                                                                                     @click="openFilter('provider_and_contract_info')"
                                                                                                                     :style="{ color: white }"/></th>
                    <th rowspan="2" style="width:7%;">Цена контракта, рублей <font-awesome-icon icon="fa-solid fa-filter"
                                                                                                @click="openFilter('contract_price')"
                                                                                                :style="{ color: white }"/></th>
                    <th rowspan="2" style="width:5%;">Заказчик</th>
                    <th rowspan="2">Дата заключения контракта/  или планируемая дата <font-awesome-icon icon="fa-solid fa-filter"
                                                                                                        @click="openFilter('date_contract_start')"
                                                                                                        :style="{ color: white }"/></th>
                    <th rowspan="2">Дата окончания контракта <font-awesome-icon icon="fa-solid fa-filter"
                                                                                @click="openFilter('date_contract_end')"
                                                                                :style="{ color: white }"/></th>
                    <th rowspan="2">Комментарий по проведенным переговорам с
                      потенциальными подрядчиками</th>
                    <th rowspan="2">Дата начала работ/Дата поставки <font-awesome-icon icon="fa-solid fa-filter"
                                                                                       @click="openFilter('date_work_start')"
                                                                                       :style="{ color: white }"/></th>
                    <th rowspan="2" style="width: 4%;">Перерасчет сметной стоимости КР в текущих ценах</th>
                    <th rowspan="2" style="width:10%;">Портал актуальной информации о ходе ремонтных работ</th>
                    <th rowspan="2" style="width: 5%;">Действия</th>
                  </tr>
                  <tr v-if="oneYearPeriod">
                    <th colspan="2">{{ getYearStartFromPeriod(selectPeriod) }}</th>
                  </tr>
                  <tr v-if="!(oneYearPeriod)">
                    <th v-if="selectPeriod == 'Все'">
                      н.р.
                    </th>
                    <th v-if="selectPeriod != 'Все'">
                      {{ getYearStartFromPeriod(selectPeriod) }}
                    </th>
                    <th v-if="selectPeriod == 'Все'">
                      о.р.
                    </th>
                    <th v-if="selectPeriod != 'Все'">
                      {{ getYearEndFromPeriod(selectPeriod) }}
                    </th>
                  </tr>
                  </thead>
                  <tbody style="font-size: 13px;">
                  <tr v-if = "LoadRecs == true">
                    <td colspan="25" style="margin: 0 auto;">
                      <img src="../../../../assets/gifs/load.gif">
                    </td>
                  </tr>
                  <tr v-if = "NewRec == true">
                    <td colspan="25" style="margin: 0 auto;">
                      <b>Новая закупка/контракт</b>
                    </td>
                  </tr>
                  <tr v-if = "NewRec == true">
                  </tr>
                  <tr v-if="NewRec == true">
                    <td>-</td>
                    <template v-if="oneYearSubsidy">
                      <td v-if="selectPeriod == 'Все'" colspan="2">{{ newRecArr[0] }}</td>
                    </template>
                    <template v-if="!(oneYearSubsidy)">
                      <td v-if="selectPeriod == 'Все'">{{ newRecArr[0] }}</td>
                      <td v-if="selectPeriod == 'Все'">{{ newRecArr[1] }}</td>
                    </template>
                    <td colspan="3">{{ newRecArr[2] }}</td>
                    <td>{{ newRecArr[3] }}</td>
                    <td>
                      <div v-if="newRecMoDocUuid == null">
                        Выберите документ МО
                      </div>
                      <div v-if="newRecMoDocUuid != null">
                        {{ newRecMoDoc }}
                      </div>
                      <a href="#" @click = "showModalAction('newMoDoc')">
                        <div style="display: inline;">
                          <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                  type="button" style="font-size: 16px;">
                            <font-awesome-icon icon="fa-solid fa-database" :style="{ color: white }"/>
                          </button>
                        </div>
                      </a>
                    </td>
                    <td>
                      <select class="form-control text-center"
                              style="font-size: 14px;"
                              v-model="newRecEventSelect"
                              @change="getSubsidyInfo('new');">
                        <option v-for="event in listEvents" :value="event.uuid">
                          {{ event.full_name }}
                        </option>
                      </select>
                    </td>
                    <template v-if="oneYearSubsidy">
                      <td style="white-space: nowrap;" colspan="2">
                        <div v-if="newRecSubsidyLoad">
                          <img src="../../../../assets/gifs/load.gif">
                        </div>
                        <div v-if="!(newRecSubsidyLoad)">
                          <money3 v-bind="money"
                                  v-model="newRecTotalYearEnd"
                                  class="form-control m-auto text-center mini-font" />
                        </div>
                      </td>
                    </template>
                    <template v-if="!(oneYearSubsidy)">
                      <td style="white-space: nowrap;">
                        <div v-if="newRecSubsidyLoad">
                          <img src="../../../../assets/gifs/load.gif">
                        </div>
                        <div v-if="!(newRecSubsidyLoad)">
                          <money3 v-bind="money"
                                  v-model="newRecTotalYearStart"
                                  class="form-control m-auto text-center mini-font" />
                        </div>
                      </td>
                      <td style="white-space: nowrap;">
                        <div v-if="newRecSubsidyLoad">
                          <img src="../../../../assets/gifs/load.gif">
                        </div>
                        <div v-if="!(newRecSubsidyLoad)">
                          <money3 v-bind="money"
                                  v-model="newRecTotalYearEnd"
                                  class="form-control m-auto text-center mini-font" />
                        </div>
                      </td>
                    </template>
                    <td>
                      <input type="date" class="form-control text-center"
                             style="font-size: 14px;"
                             v-model="newRecDateAnnounce">
                    </td>
                    <td>
                              <textarea class="form-control"
                                        style="font-size: 14px;" v-model="newRecUrlPurchase"></textarea>
                    </td>
                    <td>
                      <input type="date" class="form-control text-center"
                             style="font-size: 14px;" v-model="newRecDateAuction">
                    </td>
                    <td>
                      Заполните информацию вручную:
                      <textarea class="form-control"
                                style="font-size: 14px;" v-model="newRecProviderInfo"></textarea>
                      или выберите контракт из документов ОО<br>
                      <a href="#" @click = "showModalAction('newOoDoc')">
                        <div style="display: inline;">
                          <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                  type="button" style="font-size: 16px;">
                            <font-awesome-icon icon="fa-solid fa-database" :style="{ color: white }"/>
                          </button>
                        </div>
                      </a>
                    </td>
                    <td>
                      <div>
                        Остаток:
                        <b v-if="SubsidyInfo.balance <= 0" style="color: red;">
                          {{ String(SubsidyInfo.balance.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                        </b>
                        <b v-if="SubsidyInfo.balance > 0">
                          {{ String(SubsidyInfo.balance.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                        </b>
                        <br>
                      </div>
                      <money3 v-bind="money"
                              v-model="newRecContractPrice"
                              @change="checkContractPrice('new');"
                              class="form-control m-auto text-center mini-font" />
                      <div v-if="ContractPriceTooMuch">
                        <b style="color:red;">ВНИМАНИЕ!<br>Цена контракта<br>
                          превышает сумму<br>остаточных средств</b>
                      </div>
                    </td>
                    <td>
                        <textarea class="form-control"
                                  style="font-size: 14px;" v-model="newRecCustomer"></textarea>
                    </td>
                    <td>
                      <input type="date" class="form-control text-center"
                             style="font-size: 14px;" v-model="newRecDateContractStart">
                    </td>
                    <td>
                      <input type="date" class="form-control text-center"
                             style="font-size: 14px;" v-model="newRecDateContractEnd">
                    </td>
                    <td>
                        <textarea class="form-control"
                                  style="font-size: 14px;" v-model="newRecComment"></textarea>
                    </td>
                    <td>
                      <input type="date" class="form-control text-center"
                             style="font-size: 14px;" v-model="newRecDateWorkStart">
                    </td>
                    <td>
                      <select class="form-control text-center"
                              style="font-size: 14px;"
                              v-model="newRecRecalc">
                        <option value="true">Да</option>
                        <option value="false">Нет</option>
                      </select>
                    </td>
                    <td>
                          <textarea class="form-control"
                                    style="font-size: 14px;" v-model="newRecPortal"></textarea>
                    </td>
                    <td>
                      <div style="display: inline;">
                        <button class="btn btn-lg btn-primary iohk-butt mini-font" id="login-button"
                                type="submit">
                          <font-awesome-icon icon="fa-solid fa-check" :style="{ color: white }"/>
                        </button>
                      </div>&nbsp;
                      <a href="#" @click = "NewRec = false">
                        <div style="display: inline;">
                          <button class="btn btn-lg btn-primary iohk-butt mini-font" id="login-button"
                                  type="button">
                            <font-awesome-icon icon="fa-solid fa-xmark" :style="{ color: white }"/>
                          </button>
                        </div>
                      </a>
                    </td>
                  </tr>
                  <tr v-if = "EditRec == true">
                    <td colspan="25" style="margin: 0 auto;">
                      <b>Изменение закупки/контракта</b>
                    </td>
                  </tr>
                  <tr v-if = "EditRec == true">
                  </tr>
                  <tr v-if="EditRec == true">
                    <td>-</td>
                    <template v-if="oneYearSubsidy">
                      <td v-if="selectPeriod == 'Все'" colspan="2">{{ editRecArr[0] }}</td>
                    </template>
                    <template v-if="!(oneYearSubsidy)">
                      <td v-if="selectPeriod == 'Все'">{{ editRecArr[0] }}</td>
                      <td v-if="selectPeriod == 'Все'">{{ editRecArr[1] }}</td>
                    </template>
                    <td colspan="3">{{ editRecArr[2] }}</td>
                    <td>{{ editRecArr[3] }}</td>
                    <td>
                      <div v-if="editRecMoDocUuid == null">
                        Выберите документ МО
                      </div>
                      <div v-if="editRecMoDocUuid != null">
                        {{ editRecMoDoc }}
                      </div>
                      <a href="#" @click = "showModalAction('newMoDoc')">
                        <div style="display: inline;">
                          <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                  type="button" style="font-size: 16px;">
                            <font-awesome-icon icon="fa-solid fa-database" :style="{ color: white }"/>
                          </button>
                        </div>
                      </a>
                    </td>
                    <td>
                      <select class="form-control text-center"
                              style="font-size: 14px;"
                              v-model="editRecEventSelect"
                              @change="getSubsidyInfo('edit');">
                        <option v-for="event in listEvents" :value="event.uuid">
                          {{ event.full_name }}
                        </option>
                      </select>
                    </td>
                    <template v-if="oneYearSubsidy">
                      <td style="white-space: nowrap;" colspan="2">
                        <div v-if="newRecSubsidyLoad">
                          <img src="../../../../assets/gifs/load.gif">
                        </div>
                        <div v-if="!(newRecSubsidyLoad)">
                          <money3 v-bind="money"
                                  v-model="editRecTotalYearEnd"
                                  class="form-control m-auto text-center mini-font" />
                        </div>
                      </td>
                    </template>
                    <template v-if="!(oneYearSubsidy)">
                      <td style="white-space: nowrap;">
                        <div v-if="editRecSubsidyLoad">
                          <img src="../../../../assets/gifs/load.gif">
                        </div>
                        <div v-if="!(editRecSubsidyLoad)">
                          <money3 v-bind="money"
                                  v-model="editRecTotalYearStart"
                                  class="form-control m-auto text-center mini-font" />
                        </div>
                      </td>
                      <td style="white-space: nowrap;">
                        <div v-if="editRecSubsidyLoad">
                          <img src="../../../../assets/gifs/load.gif">
                        </div>
                        <div v-if="!(editRecSubsidyLoad)">
                          <money3 v-bind="money"
                                  v-model="editRecTotalYearEnd"
                                  class="form-control m-auto text-center mini-font" />
                        </div>
                      </td>
                    </template>
                    <td>
                      <input type="date" class="form-control text-center"
                             style="font-size: 14px;"
                             v-model="editRecDateAnnounce">
                    </td>
                    <td>
                                                      <textarea class="form-control"
                                                                style="font-size: 14px;" v-model="editRecUrlPurchase"></textarea>
                    </td>
                    <td>
                      <input type="date" class="form-control text-center"
                             style="font-size: 14px;" v-model="editRecDateAuction">
                    </td>
                    <td>
                      Измените информацию вручную:
                      <textarea class="form-control"
                                style="font-size: 14px;" v-model="editRecProviderInfo"></textarea>
                      или выберите контракт из документов ОО<br>
                      <a href="#" @click = "showModalAction('newOoDoc')">
                        <div style="display: inline;">
                          <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                  type="button" style="font-size: 16px;">
                            <font-awesome-icon icon="fa-solid fa-database" :style="{ color: white }"/>
                          </button>
                        </div>
                      </a>
                    </td>
                    <td>
                      <money3 v-bind="money"
                              v-model="editRecContractPrice"
                              @change="checkContractPrice('edit');"
                              class="form-control m-auto text-center mini-font" />
                      <div v-if="ContractPriceTooMuch">
                        <b style="color:red;">ВНИМАНИЕ!<br>Цена контракта<br>
                          превышает сумму<br>остаточных средств</b>
                      </div>
                    </td>
                    <td>
                                                      <textarea class="form-control"
                                                                style="font-size: 14px;" v-model="editRecCustomer"></textarea>
                    </td>
                    <td>
                      <input type="date" class="form-control text-center"
                             style="font-size: 14px;" v-model="editRecDateContractStart">
                    </td>
                    <td>
                      <input type="date" class="form-control text-center"
                             style="font-size: 14px;" v-model="editRecDateContractEnd">
                    </td>
                    <td>
                                                      <textarea class="form-control"
                                                                style="font-size: 14px;" v-model="editRecComment"></textarea>
                    </td>
                    <td>
                      <input type="date" class="form-control text-center"
                             style="font-size: 14px;" v-model="editRecDateWorkStart">
                    </td>
                    <td>
                      <select class="form-control text-center"
                              style="font-size: 14px;"
                              v-model="editRecRecalc">
                        <option value="true">Да</option>
                        <option value="false">Нет</option>
                      </select>
                    </td>
                    <td>
                                                      <textarea class="form-control"
                                                                style="font-size: 14px;" v-model="editRecPortal"></textarea>
                    </td>
                    <td>
                      <div style="display: inline;">
                        <button class="btn btn-lg btn-primary iohk-butt mini-font" id="login-button"
                                type="button" @click="updatePurchase();">
                          <font-awesome-icon icon="fa-solid fa-check" :style="{ color: white }"/>
                        </button>
                      </div>&nbsp;
                      <a href="#" @click = "EditRec = false">
                        <div style="display: inline;">
                          <button class="btn btn-lg btn-primary iohk-butt mini-font" id="login-button"
                                  type="button">
                            <font-awesome-icon icon="fa-solid fa-xmark" :style="{ color: white }"/>
                          </button>
                        </div>
                      </a>
                    </td>
                  </tr>
                  <template v-if="(NewRec == false) && (EditRec == false)" v-for="(rec, counter) in listRecs">
                    <tr v-if="rec.objects.length === 0">
                      <td>{{ counter+1 }}</td>
                      <template v-if="rec.year_start == rec.year_end">
                        <td  v-if="selectPeriod == 'Все'" colspan="2">
                          {{ rec.year_start }}
                        </td>
                      </template>
                      <template v-if="rec.year_start != rec.year_end">
                        <td v-if="selectPeriod == 'Все'">
                          {{ rec.year_start }}
                        </td>
                        <td v-if="selectPeriod == 'Все'">
                          {{ rec.year_end }}
                        </td>
                      </template>
                      <td>
                        {{ rec.mo_name }}<br>
                        <a href="#" @click = "editAPAction(rec.object_uuid)">
                          <div style="display: inline;">
                            <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                    type="button" style="font-size: 16px;">
                              <font-awesome-icon icon="fa-solid fa-edit" :style="{ color: white }"/>
                            </button>
                          </div>
                        </a><br><br>
                        <a href="#" @click = "deleteWK14FP(rec.object_uuid)">
                          <div style="display: inline;">
                            <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                    type="button" style="font-size: 16px;">
                              <font-awesome-icon icon="fa-solid fa-trash" :style="{ color: white }"/>
                            </button>
                          </div>
                        </a>
                      </td>
                      <td>
                        <div v-for="official in rec.officials">
                          {{ official.surname }} {{ official.name }}
                          {{ official.patronymic }},<br> {{ official.post }},<br>
                          тел.: {{ official.phone }}<br><br>
                        </div><br>
                      </td>
                      <td>
                        <div v-for="cp in rec.contact_persons">
                          {{ cp.surname }} {{ cp.name }}
                          {{ cp.patronymic }},<br>
                          тел.: {{ cp.phone }}<br><br>
                        </div><br>
                      </td>
                      <td colspan="18">
                        <b>Объекты не найдены</b>
                      </td>
                    </tr>
                    <template v-if="rec.objects.length > 0">
                      <template v-if="rec.objects[0].purchases.length === 0">
                        <tr v-if="rec.objects.length == 1">
                          <td>
                            {{ counter+1 }}
                          </td>
                          <template v-if="rec.year_start == rec.year_end">
                            <td v-if="selectPeriod == 'Все'"
                                colspan="2">
                              {{ rec.year_start }}
                            </td>
                          </template>
                          <template v-if="rec.year_start != rec.year_end">
                            <td v-if="selectPeriod == 'Все'">
                              {{ rec.year_start }}
                            </td>
                            <td v-if="selectPeriod == 'Все'">
                              {{ rec.year_end }}
                            </td>
                          </template>
                          <td>
                            {{ rec.mo_name }}<br>
                            <a href="#" @click = "editAPAction(rec.object_uuid)">
                              <div style="display: inline;">
                                <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                        type="button" style="font-size: 16px;">
                                  <font-awesome-icon icon="fa-solid fa-edit" :style="{ color: white }"/>
                                </button>
                              </div>
                            </a>
                          </td>
                          <td>
                            <div v-for="official in rec.officials">
                              {{ official.surname }} {{ official.name }}
                              {{ official.patronymic }},<br> {{ official.post }},<br>
                              тел.: {{ official.phone }}<br><br>
                            </div><br>
                          </td>
                          <td>
                            <div v-for="cp in rec.contact_persons">
                              {{ cp.surname }} {{ cp.name }}
                              {{ cp.patronymic }},<br>
                              тел.: {{ cp.phone }}<br><br>
                            </div><br>
                          </td>
                          <td v-if="!(rec.objects[0].correct)" style="background-color: #FFE6EE;">
                            {{ rec.objects[0].oo_fullname }}<br>
                            <a href="#" @click = "showNewRec(rec.object_uuid, rec.objects[0].object_uuid, rec.mo_id);">
                              <div style="display: inline;">
                                <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                        type="button" style="font-size: 16px;">
                                  <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>
                                </button>
                              </div>
                            </a>&nbsp;
                          </td>
                          <td v-if="rec.objects[0].correct">
                            {{ rec.objects[0].oo_fullname }}<br>
                            <a href="#" @click = "showNewRec(rec.object_uuid, rec.objects[0].object_uuid, rec.mo_id);">
                              <div style="display: inline;">
                                <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                        type="button" style="font-size: 16px;">
                                  <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>
                                </button>
                              </div>
                            </a>&nbsp;
                          </td>
                          <td >
                            <div v-if="getMoDocsInfo(rec.object_uuid).length > 0"
                                 v-for="mo_doc in getMoDocsInfo(rec.object_uuid)">
                              <a href="#" @click="showDoc(mo_doc[0], 'mo');">
                                {{ mo_doc[1] }}
                              </a><br><br>
                            </div>
                            <div v-if="getMoDocsInfo(rec.object_uuid).length == 0">
                              -
                            </div>
                          </td>
                          <td colspan="16">
                            <b>Закупки не найдены</b>
                          </td>
                        </tr>
                        <tr v-if="rec.objects.length > 1">
                          <td :rowspan="getRowsSpanMo(rec.object_uuid)">{{ counter+1 }}</td>
                          <template v-if="rec.year_start == rec.year_end">
                            <td :rowspan="getRowsSpanMo(rec.object_uuid)"
                                v-if="selectPeriod == 'Все'" colspan="2">
                              {{ rec.year_start }}
                            </td>
                          </template>
                          <template v-if="rec.year_start != rec.year_end">
                            <td :rowspan="getRowsSpanMo(rec.object_uuid)"
                                v-if="selectPeriod == 'Все'">
                              {{ rec.year_start }}
                            </td>
                            <td :rowspan="getRowsSpanMo(rec.object_uuid)"
                                v-if="selectPeriod == 'Все'">
                              {{ rec.year_end }}
                            </td>
                          </template>
                          <td :rowspan="getRowsSpanMo(rec.object_uuid)">
                            {{ rec.mo_name }}<br>
                            <a href="#" @click = "editAPAction(rec.object_uuid)">
                              <div style="display: inline;">
                                <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                        type="button" style="font-size: 16px;">
                                  <font-awesome-icon icon="fa-solid fa-edit" :style="{ color: white }"/>
                                </button>
                              </div>
                            </a>
                          </td>
                          <td :rowspan="getRowsSpanMo(rec.object_uuid)">
                            <div v-for="official in rec.officials">
                              {{ official.surname }} {{ official.name }}
                              {{ official.patronymic }},<br> {{ official.post }},<br>
                              тел.: {{ official.phone }}<br><br>
                            </div><br>
                          </td>
                          <td :rowspan="getRowsSpanMo(rec.object_uuid)">
                            <div v-for="cp in rec.contact_persons">
                              {{ cp.surname }} {{ cp.name }}
                              {{ cp.patronymic }},<br>
                              тел.: {{ cp.phone }}<br><br>
                            </div><br>
                          </td>
                          <td :rowspan="getRowsSpanObject(rec.object_uuid, rec.objects[0].object_uuid)" v-if="!(rec.objects[0].correct)" style="background-color: #FFE6EE;">
                            {{ rec.objects[0].oo_fullname }}<br>
                            <a href="#" @click = "showNewRec(rec.object_uuid, rec.objects[0].object_uuid, rec.mo_id);">
                              <div style="display: inline;">
                                <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                        type="button" style="font-size: 16px;">
                                  <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>
                                </button>
                              </div>
                            </a>&nbsp;
                          </td>
                          <td :rowspan="getRowsSpanObject(rec.object_uuid, rec.objects[0].object_uuid)" v-if="rec.objects[0].correct">
                            {{ rec.objects[0].oo_fullname }}<br>
                            <a href="#" @click = "showNewRec(rec.object_uuid, rec.objects[0].object_uuid, rec.mo_id);">
                              <div style="display: inline;">
                                <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                        type="button" style="font-size: 16px;">
                                  <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>
                                </button>
                              </div>
                            </a>&nbsp;
                          </td>
                          <td :rowspan="getRowsSpanMo(rec.object_uuid)">
                            <div v-if="getMoDocsInfo(rec.object_uuid).length > 0"
                                 v-for="mo_doc in getMoDocsInfo(rec.object_uuid)">
                              <a href="#" @click="showDoc(mo_doc[0], 'mo');">
                                {{ mo_doc[1] }}
                              </a><br><br>
                            </div>
                            <div v-if="getMoDocsInfo(rec.object_uuid).length == 0">
                              -
                            </div>
                          </td>
                          <td :rowspan="getRowsSpanObject(rec.object_uuid, rec.objects[0].object_uuid)"
                              colspan="16">
                            <b>Закупки не найдены</b>
                          </td>
                        </tr>
                      </template>
                      <template v-if="rec.objects[0].purchases.length !== 0">
                        <tr v-if="rec.objects.length == 1">
                          <td :rowspan="getRowsSpanMo(rec.object_uuid)">{{ counter+1 }}</td>
                          <template v-if="rec.year_start == rec.year_end">
                            <td :rowspan="getRowsSpanObject(rec.object_uuid, rec.objects[0].object_uuid)"
                                v-if="selectPeriod == 'Все'" colspan="2">
                              {{ rec.year_start }}
                            </td>
                          </template>
                          <template v-if="rec.year_start != rec.year_end">
                            <td :rowspan="getRowsSpanMo(rec.object_uuid)"
                                v-if="selectPeriod == 'Все'">
                              {{ rec.year_start }}
                            </td>
                            <td :rowspan="getRowsSpanMo(rec.object_uuid)"
                                v-if="selectPeriod == 'Все'">
                              {{ rec.year_end }}
                            </td>
                          </template>
                          <td :rowspan="getRowsSpanMo(rec.object_uuid)">
                            {{ rec.mo_name }}<br>
                            <a href="#" @click = "editAPAction(rec.object_uuid)">
                              <div style="display: inline;">
                                <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                        type="button" style="font-size: 16px;">
                                  <font-awesome-icon icon="fa-solid fa-edit" :style="{ color: white }"/>
                                </button>
                              </div>
                            </a>
                          </td>
                          <td :rowspan="getRowsSpanMo(rec.object_uuid)">
                            <div v-for="official in rec.officials">
                              {{ official.surname }} {{ official.name }}
                              {{ official.patronymic }},<br> {{ official.post }},<br>
                              тел.: {{ official.phone }}<br><br>
                            </div><br>
                          </td>
                          <td :rowspan="getRowsSpanMo(rec.object_uuid)">
                            <div v-for="cp in rec.contact_persons">
                              {{ cp.surname }} {{ cp.name }}
                              {{ cp.patronymic }},<br>
                              тел.: {{ cp.phone }}<br><br>
                            </div><br>
                          </td>
                          <td :rowspan="getRowsSpanObject(rec.object_uuid, rec.objects[0].object_uuid)" v-if="!(rec.objects[0].correct)" style="background-color: #FFE6EE;">
                            {{ rec.objects[0].oo_fullname }}<br>
                            <a href="#" @click = "showNewRec(rec.object_uuid, rec.objects[0].object_uuid, rec.mo_id);">
                              <div style="display: inline;">
                                <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                        type="button" style="font-size: 16px;">
                                  <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>
                                </button>
                              </div>
                            </a>&nbsp;
                          </td>
                          <td :rowspan="getRowsSpanObject(rec.object_uuid, rec.objects[0].object_uuid)" v-if="rec.objects[0].correct">
                            {{ rec.objects[0].oo_fullname }}<br>
                            <a href="#" @click = "showNewRec(rec.object_uuid, rec.objects[0].object_uuid, rec.mo_id);">
                              <div style="display: inline;">
                                <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                        type="button" style="font-size: 16px;">
                                  <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>
                                </button>
                              </div>
                            </a>&nbsp;
                          </td>
                          <td :rowspan="getRowsSpanMo(rec.object_uuid)">
                            <div v-if="getMoDocsInfo(rec.object_uuid).length > 0"
                                 v-for="mo_doc in getMoDocsInfo(rec.object_uuid)">
                              <a href="#" @click="showDoc(mo_doc[0], 'mo');">
                                {{ mo_doc[1] }}
                              </a><br><br>
                            </div>
                            <div v-if="getMoDocsInfo(rec.object_uuid).length == 0">
                              -
                            </div>
                          </td>
                          <td>
                            {{ rec.objects[0].purchases[0].event_name }}
                            <div v-if="rec.objects[0].purchases[0].changes.length > 0">
                              <a href="#"
                                 @click="showVersions(rec.object_uuid, rec.objects[0].object_uuid, rec.objects[0].purchases[0].object_uuid)">
                                <b>Версии</b>
                              </a>
                            </div>
                          </td>
                          <template v-if="rec.year_start == rec.year_end">
                            <td style="white-space: nowrap;" :rowspan="rec.objects[0].purchases.filter((purch) => purch.event_name === rec.objects[0].purchases[0].event_name).length"
                                colspan="2">
                              {{ String(rec.objects[0].purchases[0].event_grant_end.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                            </td>
                          </template>
                          <template v-if="rec.year_start != rec.year_end">
                            <td style="white-space: nowrap;" :rowspan="rec.objects[0].purchases.filter((purch) => purch.event_name === rec.objects[0].purchases[0].event_name).length">
                              {{ String(rec.objects[0].purchases[0].event_grant_start.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                            </td>
                            <td style="white-space: nowrap;" :rowspan="rec.objects[0].purchases.filter((purch) => purch.event_name === rec.objects[0].purchases[0].event_name).length">
                              {{ String(rec.objects[0].purchases[0].event_grant_end.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                            </td>
                          </template>
                          <td>
                            <div v-if="rec.objects[0].purchases[0].date_announce != null">
                              {{ format(rec.objects[0].purchases[0].date_announce) }}
                            </div>
                            <div v-if="rec.objects[0].purchases[0].date_announce == null">
                              -
                            </div>
                          </td>
                          <td style="width: 300px; overflow-wrap: normal;">
                            <div v-if="checkUrl(rec.objects[0].purchases[0].url_purchase)">
                              <a :href="rec.objects[0].purchases[0].url_purchase" target="_blank">
                                {{ rec.objects[0].purchases[0].url_purchase }}
                              </a>
                            </div>
                            <div v-if="!(checkUrl(rec.objects[0].purchases[0].url_purchase))">
                              {{ rec.objects[0].purchases[0].url_purchase }}
                            </div>
                          </td>
                          <td>
                            <div v-if="rec.objects[0].purchases[0].date_auction != null">
                              {{ format(rec.objects[0].purchases[0].date_auction) }}
                            </div>
                            <div v-if="rec.objects[0].purchases[0].date_auction == null">
                              -
                            </div>
                          </td>
                          <td>
                            <div v-if="rec.objects[0].purchases[0].contract_id != null">
                              <a href="#" @click="showDoc(rec.objects[0].purchases[0].contract_id, 'regular');">
                                {{ rec.objects[0].purchases[0].provider_and_contract_info }}
                              </a>
                            </div>
                            <div v-if="rec.objects[0].purchases[0].contract_id == null">
                              {{ rec.objects[0].purchases[0].provider_and_contract_info }}
                            </div>
                          </td>
                          <td style="white-space: nowrap;">
                            {{ String(rec.objects[0].purchases[0].contract_price.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                          </td>
                          <td>
                            {{ rec.objects[0].purchases[0].customer }}
                          </td>
                          <td>
                            <div v-if="rec.objects[0].purchases[0].date_contract_start != null">
                              {{ format(rec.objects[0].purchases[0].date_contract_start) }}
                            </div>
                            <div v-if="rec.objects[0].purchases[0].date_contract_start == null">
                              -
                            </div>
                          </td>
                          <td>
                            <div v-if="rec.objects[0].purchases[0].date_contract_end != null">
                              {{ format(rec.objects[0].purchases[0].date_contract_end) }}
                            </div>
                            <div v-if="rec.objects[0].purchases[0].date_contract_end == null">
                              -
                            </div>
                          </td>
                          <td>
                            {{ rec.objects[0].purchases[0].comment }}
                          </td>
                          <td>
                            <div v-if="rec.objects[0].purchases[0].date_work_start != null">
                              {{ format(rec.objects[0].purchases[0].date_work_start) }}
                            </div>
                            <div v-if="rec.objects[0].purchases[0].date_work_start == null">
                              -
                            </div>
                          </td>
                          <td>
                            <div v-if="rec.objects[0].purchases[0].recalc == true">
                              <b>Да</b>
                            </div>
                            <div v-if="rec.objects[0].purchases[0].recalc == false">
                              <b>Нет</b>
                            </div>
                          </td>
                          <td>
                            <a :href="rec.objects[0].purchases[0].portal"
                               target="_blank">
                              {{ rec.objects[0].purchases[0].portal }}
                            </a>
                          </td>
                          <td style="width: 3%;">
                            <a href="#" @click = "showEditForm(rec.objects[0].purchases[0].object_uuid, rec.object_uuid, rec.objects[0].object_uuid, rec.mo_id);" style="color: #373c59;">
                              <font-awesome-icon icon="fa-solid fa-pen-to-square" size="2x" />
                            </a>&nbsp;&nbsp;&nbsp;
                            <a href="#" @click = "deletePurchase(rec.objects[0].purchases[0].object_uuid);" style="color: #373c59;">
                              <font-awesome-icon icon="fa-solid fa-trash" size="2x" />
                            </a>
                          </td>
                        </tr>
                        <tr v-if="rec.objects.length > 1">
                          <td :rowspan="getRowsSpanMo(rec.object_uuid)">{{ counter+1 }}</td>
                          <template v-if="rec.year_start == rec.year_end">
                            <td :rowspan="getRowsSpanMo(rec.object_uuid)"
                                v-if="selectPeriod == 'Все'" colspan="2">
                              {{ rec.year_start }}
                            </td>
                          </template>
                          <template v-if="rec.year_start != rec.year_end">
                            <td :rowspan="getRowsSpanMo(rec.object_uuid)"
                                v-if="selectPeriod == 'Все'">
                              {{ rec.year_start }}
                            </td>
                            <td :rowspan="getRowsSpanMo(rec.object_uuid)"
                                v-if="selectPeriod == 'Все'">
                              {{ rec.year_end }}
                            </td>
                          </template>
                          <td :rowspan="getRowsSpanMo(rec.object_uuid)">
                            {{ rec.mo_name }}<br>
                            <a href="#" @click = "editAPAction(rec.object_uuid)">
                              <div style="display: inline;">
                                <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                        type="button" style="font-size: 16px;">
                                  <font-awesome-icon icon="fa-solid fa-edit" :style="{ color: white }"/>
                                </button>
                              </div>
                            </a>
                          </td>
                          <td :rowspan="getRowsSpanMo(rec.object_uuid)">
                            <div v-for="official in rec.officials">
                              {{ official.surname }} {{ official.name }}
                              {{ official.patronymic }},<br> {{ official.post }},<br>
                              тел.: {{ official.phone }}<br><br>
                            </div><br>
                          </td>
                          <td :rowspan="getRowsSpanMo(rec.object_uuid)">
                            <div v-for="cp in rec.contact_persons">
                              {{ cp.surname }} {{ cp.name }}
                              {{ cp.patronymic }},<br>
                              тел.: {{ cp.phone }}<br><br>
                            </div><br>
                          </td>
                          <td :rowspan="getRowsSpanObject(rec.object_uuid, rec.objects[0].object_uuid)" v-if="!(rec.objects[0].correct)" style="background-color: #FFE6EE;">
                            {{ rec.objects[0].oo_fullname }}<br>
                            <a href="#" @click = "showNewRec(rec.object_uuid, rec.objects[0].object_uuid, rec.mo_id);">
                              <div style="display: inline;">
                                <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                        type="button" style="font-size: 16px;">
                                  <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>
                                </button>
                              </div>
                            </a>&nbsp;
                          </td>
                          <td :rowspan="getRowsSpanObject(rec.object_uuid, rec.objects[0].object_uuid)" v-if="rec.objects[0].correct">
                            {{ rec.objects[0].oo_fullname }}<br>
                            <a href="#" @click = "showNewRec(rec.object_uuid, rec.objects[0].object_uuid, rec.mo_id);">
                              <div style="display: inline;">
                                <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                        type="button" style="font-size: 16px;">
                                  <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>
                                </button>
                              </div>
                            </a>&nbsp;
                          </td>
                          <td :rowspan="getRowsSpanMo(rec.object_uuid)">
                            <div v-if="getMoDocsInfo(rec.object_uuid).length > 0"
                                 v-for="mo_doc in getMoDocsInfo(rec.object_uuid)">
                              <a href="#" @click="showDoc(mo_doc[0], 'mo');">
                                {{ mo_doc[1] }}
                              </a><br><br>
                            </div>
                            <div v-if="getMoDocsInfo(rec.object_uuid).length == 0">
                              -
                            </div>
                          </td>
                          <td>
                            {{ rec.objects[0].purchases[0].event_name }}
                            <div v-if="rec.objects[0].purchases[0].changes.length > 0">
                              <a href="#"
                                 @click="showVersions(rec.object_uuid, rec.objects[0].object_uuid, rec.objects[0].purchases[0].object_uuid)">
                                <b>Версии</b>
                              </a>
                            </div>
                          </td>
                          <template v-if="rec.year_start == rec.year_end">
                            <td style="white-space: nowrap;" colspan="2" :rowspan="rec.objects[0].purchases.filter((purch) => purch.event_name === rec.objects[0].purchases[0].event_name).length">
                              {{ String(rec.objects[0].purchases[0].event_grant_end.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                            </td>
                          </template>
                          <template v-if="rec.year_start != rec.year_end">
                            <td style="white-space: nowrap;" :rowspan="rec.objects[0].purchases.filter((purch) => purch.event_name === rec.objects[0].purchases[0].event_name).length">
                              {{ String(rec.objects[0].purchases[0].event_grant_start.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                            </td>
                            <td style="white-space: nowrap;" :rowspan="rec.objects[0].purchases.filter((purch) => purch.event_name === rec.objects[0].purchases[0].event_name).length">
                              {{ String(rec.objects[0].purchases[0].event_grant_end.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                            </td>
                          </template>
                          <td>
                            <div v-if="rec.objects[0].purchases[0].date_announce != null">
                              {{ format(rec.objects[0].purchases[0].date_announce) }}
                            </div>
                            <div v-if="rec.objects[0].purchases[0].date_announce == null">
                              -
                            </div>
                          </td>
                          <td style="width: 300px; overflow-wrap: normal;">
                            <div v-if="checkUrl(rec.objects[0].purchases[0].url_purchase)">
                              <a :href="rec.objects[0].purchases[0].url_purchase" target="_blank">
                                {{ rec.objects[0].purchases[0].url_purchase }}
                              </a>
                            </div>
                            <div v-if="!(checkUrl(rec.objects[0].purchases[0].url_purchase))">
                              {{ rec.objects[0].purchases[0].url_purchase }}
                            </div>
                          </td>
                          <td>
                            <div v-if="rec.objects[0].purchases[0].date_auction != null">
                              {{ format(rec.objects[0].purchases[0].date_auction) }}
                            </div>
                            <div v-if="rec.objects[0].purchases[0].date_auction == null">
                              -
                            </div>
                          </td>
                          <td>
                            <div v-if="rec.objects[0].purchases[0].contract_id != null">
                              <a href="#" @click="showDoc(rec.objects[0].purchases[0].contract_id, 'regular');">
                                {{ rec.objects[0].purchases[0].provider_and_contract_info }}
                              </a>
                            </div>
                            <div v-if="rec.objects[0].purchases[0].contract_id == null">
                              {{ rec.objects[0].purchases[0].provider_and_contract_info }}
                            </div>
                          </td>
                          <td style="white-space: nowrap;">
                            {{ String(rec.objects[0].purchases[0].contract_price.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                          </td>
                          <td>
                            {{ rec.objects[0].purchases[0].customer }}
                          </td>
                          <td>
                            <div v-if="rec.objects[0].purchases[0].date_contract_start != null">
                              {{ format(rec.objects[0].purchases[0].date_contract_start) }}
                            </div>
                            <div v-if="rec.objects[0].purchases[0].date_contract_start == null">
                              -
                            </div>
                          </td>
                          <td>
                            <div v-if="rec.objects[0].purchases[0].date_contract_end != null">
                              {{ format(rec.objects[0].purchases[0].date_contract_end) }}
                            </div>
                            <div v-if="rec.objects[0].purchases[0].date_contract_end == null">
                              -
                            </div>
                          </td>
                          <td>
                            {{ rec.objects[0].purchases[0].comment }}
                          </td>
                          <td>
                            <div v-if="rec.objects[0].purchases[0].date_work_start != null">
                              {{ format(rec.objects[0].purchases[0].date_work_start) }}
                            </div>
                            <div v-if="rec.objects[0].purchases[0].date_work_start == null">
                              -
                            </div>
                          </td>
                          <td>
                            <div v-if="rec.objects[0].purchases[0].recalc == true">
                              <b>Да</b>
                            </div>
                            <div v-if="rec.objects[0].purchases[0].recalc == false">
                              <b>Нет</b>
                            </div>
                          </td>
                          <td>
                            <a :href="rec.objects[0].purchases[0].portal"
                               target="_blank">
                              {{ rec.objects[0].purchases[0].portal }}
                            </a>
                          </td>
                          <td style="width: 3%;">
                            <a href="#" @click = "showEditForm(rec.objects[0].purchases[0].object_uuid, rec.object_uuid, rec.objects[0].object_uuid, rec.mo_id);" style="color: #373c59;">
                              <font-awesome-icon icon="fa-solid fa-pen-to-square" size="2x" />
                            </a>&nbsp;&nbsp;&nbsp;
                            <a href="#" @click = "deletePurchase(rec.objects[0].purchases[0].object_uuid);" style="color: #373c59;">
                              <font-awesome-icon icon="fa-solid fa-trash" size="2x" />
                            </a>
                          </td>
                        </tr>
                        <template v-if="rec.objects[0].purchases.length > 1">
                          <template v-for="(purchase, p_counter) in rec.objects[0].purchases">
                            <tr v-if="p_counter > 0">
                              <td>
                                {{ purchase.event_name }}
                                <div v-if="purchase.changes.length > 0">
                                  <a href="#"
                                     @click="showVersions(rec.object_uuid, rec.objects[0].object_uuid, purchase.object_uuid)">
                                    <b>Версии</b>
                                  </a>
                                </div>
                              </td>
                              <template v-if="(rec.year_start == rec.year_end) &&
                                              (purchase.event_name !== rec.objects[0].purchases[0].event_name) &&
                                              (rec.objects[0].purchases.filter((purch) => purch.event_name === purchase.event_name)[0].object_uuid === purchase.object_uuid)">
                                <td style="white-space: nowrap;" colspan="2" :rowspan="rec.objects[0].purchases.filter((purch) => purch.event_name === purchase.event_name).length">
                                  {{ String(purchase.event_grant_end.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                                </td>
                              </template>
                              <template v-if="(rec.year_start != rec.year_end) &&
                                              (purchase.event_name !== rec.objects[0].purchases[0].event_name) &&
                                              (rec.objects[0].purchases.filter((purch) => purch.event_name === purchase.event_name)[0].object_uuid === purchase.object_uuid)">
                                <td style="white-space: nowrap;" :rowspan="rec.objects[0].purchases.filter((purch) => purch.event_name === purchase.event_name).length">
                                  {{ String(purchase.event_grant_start.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                                </td>
                                <td style="white-space: nowrap;" :rowspan="rec.objects[0].purchases.filter((purch) => purch.event_name === purchase.event_name).length">
                                  {{ String(purchase.event_grant_end.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                                </td>
                              </template>
                              <td>
                                <div v-if="purchase.date_announce != null">
                                  {{ format(purchase.date_announce) }}
                                </div>
                                <div v-if="purchase.date_announce == null">
                                  -
                                </div>
                              </td>
                              <td style="width: 300px; overflow-wrap: normal;">
                                <div v-if="checkUrl(purchase.url_purchase)">
                                  <a :href="purchase.url_purchase" target="_blank">
                                    {{ purchase.url_purchase }}
                                  </a>
                                </div>
                                <div v-if="!(checkUrl(purchase.url_purchase))">
                                  {{ purchase.url_purchase }}
                                </div>
                              </td>
                              <td>
                                <div v-if="purchase.date_auction != null">
                                  {{ format(purchase.date_auction) }}
                                </div>
                                <div v-if="purchase.date_auction == null">
                                  -
                                </div>
                              </td>
                              <td>
                                <div v-if="purchase.contract_id != null">
                                  <a href="#" @click="showDoc(purchase.contract_id, 'regular');">
                                    {{ purchase.provider_and_contract_info }}
                                  </a>
                                </div>
                                <div v-if="purchase.contract_id == null">
                                  {{ purchase.provider_and_contract_info }}
                                </div>
                              </td>
                              <td style="white-space: nowrap;">
                                {{ String(purchase.contract_price.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                              </td>
                              <td>
                                {{ purchase.customer }}
                              </td>
                              <td>
                                <div v-if="purchase.date_contract_start != null">
                                  {{ format(purchase.date_contract_start) }}
                                </div>
                                <div v-if="purchase.date_contract_start == null">
                                  -
                                </div>
                              </td>
                              <td>
                                <div v-if="purchase.date_contract_end != null">
                                  {{ format(purchase.date_contract_end) }}
                                </div>
                                <div v-if="purchase.date_contract_end == null">
                                  -
                                </div>
                              </td>
                              <td>
                                {{ purchase.comment }}
                              </td>
                              <td>
                                <div v-if="purchase.date_work_start != null">
                                  {{ format(purchase.date_work_start) }}
                                </div>
                                <div v-if="purchase.date_work_start == null">
                                  -
                                </div>
                              </td>
                              <td>
                                <div v-if="purchase.recalc == true">
                                  <b>Да</b>
                                </div>
                                <div v-if="purchase.recalc == false">
                                  <b>Нет</b>
                                </div>
                              </td>
                              <td>
                                <a :href="purchase.portal"
                                   target="_blank">
                                  {{ purchase.portal }}
                                </a>
                              </td>
                              <td style="width: 3%;">
                                <a href="#" @click = "showEditForm(purchase.object_uuid, rec.object_uuid, rec.objects[0].object_uuid, rec.mo_id);" style="color: #373c59;">
                                  <font-awesome-icon icon="fa-solid fa-pen-to-square" size="2x" />
                                </a>&nbsp;&nbsp;&nbsp;
                                <a href="#" @click = "deletePurchase(purchase.object_uuid);" style="color: #373c59;">
                                  <font-awesome-icon icon="fa-solid fa-trash" size="2x" />
                                </a>
                              </td>
                            </tr>
                          </template>
                        </template>
                      </template>
                      <template v-if="rec.objects.length > 1">
                        <template v-for="(obj, obj_counter) in rec.objects">
                          <template v-if="obj_counter > 0">

                            <tr v-if="obj.purchases.length === 0">
                              <td :rowspan="getRowsSpanObject(rec.object_uuid, obj.object_uuid)" v-if="!(obj.correct)" style="background-color: #FFE6EE;">
                                {{ obj.oo_fullname }}<br>
                                <a href="#" @click = "showNewRec(rec.object_uuid, obj.object_uuid, rec.mo_id);">
                                  <div style="display: inline;">
                                    <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                            type="button" style="font-size: 16px;">
                                      <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>
                                    </button>
                                  </div>
                                </a>&nbsp;
                              </td>
                              <td :rowspan="getRowsSpanObject(rec.object_uuid, obj.object_uuid)" v-if="obj.correct">
                                {{ obj.oo_fullname }}<br>
                                <a href="#" @click = "showNewRec(rec.object_uuid, obj.object_uuid, rec.mo_id);">
                                  <div style="display: inline;">
                                    <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                            type="button" style="font-size: 16px;">
                                      <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>
                                    </button>
                                  </div>
                                </a>&nbsp;
                              </td>
                              <td colspan="16">
                                <b>Закупки не найдены</b>
                              </td>
                            </tr>

                            <template v-if="obj.purchases.length > 0">
                              <tr>
                                <td :rowspan="getRowsSpanObject(rec.object_uuid, obj.object_uuid)" v-if="!(obj.correct)" style="background-color: #FFE6EE;">
                                  {{ obj.oo_fullname }}<br>
                                  <a href="#" @click = "showNewRec(rec.object_uuid, obj.object_uuid, rec.mo_id);">
                                    <div style="display: inline;">
                                      <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                              type="button" style="font-size: 16px;">
                                        <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>
                                      </button>
                                    </div>
                                  </a>&nbsp;
                                </td>
                                <td :rowspan="getRowsSpanObject(rec.object_uuid, obj.object_uuid)" v-if="obj.correct">
                                  {{ obj.oo_fullname }}<br>
                                  <a href="#" @click = "showNewRec(rec.object_uuid, obj.object_uuid, rec.mo_id);">
                                    <div style="display: inline;">
                                      <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                              type="button" style="font-size: 16px;">
                                        <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>
                                      </button>
                                    </div>
                                  </a>&nbsp;
                                </td>
                                <td>
                                  {{ obj.purchases[0].event_name }}
                                  <div v-if="obj.purchases[0].changes.length > 0">
                                    <a href="#"
                                       @click="showVersions(rec.object_uuid, obj.object_uuid, obj.purchases[0].object_uuid)">
                                      <b>Версии</b>
                                    </a>
                                  </div>
                                </td>
                                <template v-if="rec.year_start == rec.year_end">
                                  <td style="white-space: nowrap;" colspan="2" :rowspan="obj.purchases.filter((purch) => purch.event_name === obj.purchases[0].event_name).length">
                                    {{ String(obj.purchases[0].event_grant_end.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                                  </td>
                                </template>
                                <template v-if="rec.year_start != rec.year_end">
                                  <td style="white-space: nowrap;" :rowspan="obj.purchases.filter((purch) => purch.event_name === obj.purchases[0].event_name).length">
                                    {{ String(obj.purchases[0].event_grant_start.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                                  </td>
                                  <td style="white-space: nowrap;" :rowspan="obj.purchases.filter((purch) => purch.event_name === obj.purchases[0].event_name).length">
                                    {{ String(obj.purchases[0].event_grant_end.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                                  </td>
                                </template>
                                <td>
                                  <div v-if="obj.purchases[0].date_announce != null">
                                    {{ format(obj.purchases[0].date_announce) }}
                                  </div>
                                  <div v-if="obj.purchases[0].date_announce == null">
                                    -
                                  </div>
                                </td>
                                <td style="width: 300px; overflow-wrap: normal;">
                                  <div v-if="checkUrl(obj.purchases[0].url_purchase)">
                                    <a :href="obj.purchases[0].url_purchase" target="_blank">
                                      {{ obj.purchases[0].url_purchase }}
                                    </a>
                                  </div>
                                  <div v-if="!(checkUrl(obj.purchases[0].url_purchase))">
                                    {{ obj.purchases[0].url_purchase }}
                                  </div>
                                </td>
                                <td>
                                  <div v-if="obj.purchases[0].date_auction != null">
                                    {{ format(obj.purchases[0].date_auction) }}
                                  </div>
                                  <div v-if="obj.purchases[0].date_auction == null">
                                    -
                                  </div>
                                </td>
                                <td>
                                  <div v-if="obj.purchases[0].contract_id != null">
                                    <a href="#" @click="showDoc(obj.purchases[0].contract_id, 'regular');">
                                      {{ obj.purchases[0].provider_and_contract_info }}
                                    </a>
                                  </div>
                                  <div v-if="obj.purchases[0].contract_id == null">
                                    {{ obj.purchases[0].provider_and_contract_info }}
                                  </div>
                                </td>
                                <td style="white-space: nowrap;">
                                  {{ String(obj.purchases[0].contract_price.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                                </td>
                                <td>
                                  {{ obj.purchases[0].customer }}
                                </td>
                                <td>
                                  <div v-if="obj.purchases[0].date_contract_start != null">
                                    {{ format(obj.purchases[0].date_contract_start) }}
                                  </div>
                                  <div v-if="obj.purchases[0].date_contract_start == null">
                                    -
                                  </div>
                                </td>
                                <td>
                                  <div v-if="obj.purchases[0].date_contract_end != null">
                                    {{ format(obj.purchases[0].date_contract_end) }}
                                  </div>
                                  <div v-if="obj.purchases[0].date_contract_end == null">
                                    -
                                  </div>
                                </td>
                                <td>
                                  {{ obj.purchases[0].comment }}
                                </td>
                                <td>
                                  <div v-if="obj.purchases[0].date_work_start != null">
                                    {{ format(obj.purchases[0].date_work_start) }}
                                  </div>
                                  <div v-if="obj.purchases[0].date_work_start == null">
                                    -
                                  </div>
                                </td>
                                <td>
                                  <div v-if="obj.purchases[0].recalc == true">
                                    <b>Да</b>
                                  </div>
                                  <div v-if="obj.purchases[0].recalc == false">
                                    <b>Нет</b>
                                  </div>
                                </td>
                                <td>
                                  <a :href="obj.purchases[0].portal"
                                     target="_blank">
                                    {{ obj.purchases[0].portal }}
                                  </a>
                                </td>
                                <td style="width: 3%;">
                                  <a href="#" @click = "showEditForm(obj.purchases[0].object_uuid, rec.object_uuid, obj.object_uuid, rec.mo_id);" style="color: #373c59;">
                                    <font-awesome-icon icon="fa-solid fa-pen-to-square" size="2x" />
                                  </a>&nbsp;&nbsp;&nbsp;
                                  <a href="#" @click = "deletePurchase(obj.purchases[0].object_uuid);" style="color: #373c59;">
                                    <font-awesome-icon icon="fa-solid fa-trash" size="2x" />
                                  </a>
                                </td>
                              </tr>

                              <template v-if="obj.purchases.length > 1">
                                <template v-for="(purchase, p_counter) in obj.purchases">
                                  <tr v-if="p_counter>0">
                                    <td>
                                      {{ purchase.event_name }}
                                      <div v-if="purchase.changes.length > 0">
                                        <a href="#"
                                           @click="showVersions(rec.object_uuid, rec.objects[0].object_uuid, purchase.object_uuid)">
                                          <b>Версии</b>
                                        </a>
                                      </div>
                                    </td>
                                    <template v-if="(rec.year_start == rec.year_end) && (purchase.event_name !== obj.purchases[0].event_name)">
                                      <td style="white-space: nowrap;" colspan="2" :rowspan="obj.purchases.filter((purch) => purch.event_name === purchase.event_name).length">
                                        {{ String(purchase.event_grant_end.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                                      </td>
                                    </template>
                                    <template v-if="(rec.year_start != rec.year_end) && (purchase.event_name !== obj.purchases[0].event_name)">
                                      <td style="white-space: nowrap;" :rowspan="obj.purchases.filter((purch) => purch.event_name === purchase.event_name).length">
                                        {{ String(purchase.event_grant_start.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                                      </td>
                                      <td style="white-space: nowrap;" :rowspan="obj.purchases.filter((purch) => purch.event_name === purchase.event_name).length">
                                        {{ String(purchase.event_grant_end.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                                      </td>
                                    </template>
                                    <td>
                                      <div v-if="purchase.date_announce != null">
                                        {{ format(purchase.date_announce) }}
                                      </div>
                                      <div v-if="purchase.date_announce == null">
                                        -
                                      </div>
                                    </td>
                                    <td style="width: 300px; overflow-wrap: normal;">
                                      <div v-if="checkUrl(purchase.url_purchase)">
                                        <a :href="purchase.url_purchase" target="_blank">
                                          {{ purchase.url_purchase }}
                                        </a>
                                      </div>
                                      <div v-if="!(checkUrl(purchase.url_purchase))">
                                        {{ purchase.url_purchase }}
                                      </div>
                                    </td>
                                    <td>
                                      <div v-if="purchase.date_auction != null">
                                        {{ format(purchase.date_auction) }}
                                      </div>
                                      <div v-if="purchase.date_auction == null">
                                        -
                                      </div>
                                    </td>
                                    <td>
                                      <div v-if="purchase.contract_id != null">
                                        <a href="#" @click="showDoc(purchase.contract_id, 'regular');">
                                          {{ purchase.provider_and_contract_info }}
                                        </a>
                                      </div>
                                      <div v-if="purchase.contract_id == null">
                                        {{ purchase.provider_and_contract_info }}
                                      </div>
                                    </td>
                                    <td style="white-space: nowrap;">
                                      {{ String(purchase.contract_price.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
                                    </td>
                                    <td>
                                      {{ purchase.customer }}
                                    </td>
                                    <td>
                                      <div v-if="purchase.date_contract_start != null">
                                        {{ format(purchase.date_contract_start) }}
                                      </div>
                                      <div v-if="purchase.date_contract_start == null">
                                        -
                                      </div>
                                    </td>
                                    <td>
                                      <div v-if="purchase.date_contract_end != null">
                                        {{ format(purchase.date_contract_end) }}
                                      </div>
                                      <div v-if="purchase.date_contract_end == null">
                                        -
                                      </div>
                                    </td>
                                    <td>
                                      {{ purchase.comment }}
                                    </td>
                                    <td>
                                      <div v-if="purchase.date_work_start != null">
                                        {{ format(purchase.date_work_start) }}
                                      </div>
                                      <div v-if="purchase.date_work_start == null">
                                        -
                                      </div>
                                    </td>
                                    <td>
                                      <div v-if="purchase.recalc == true">
                                        <b>Да</b>
                                      </div>
                                      <div v-if="purchase.recalc == false">
                                        <b>Нет</b>
                                      </div>
                                    </td>
                                    <td>
                                      <a :href="purchase.portal"
                                         target="_blank">
                                        {{ purchase.portal }}
                                      </a>
                                    </td>
                                    <td style="width: 3%;">
                                      <a href="#" @click = "showEditForm(purchase.object_uuid, rec.object_uuid, rec.objects[0].object_uuid, rec.mo_id);" style="color: #373c59;">
                                        <font-awesome-icon icon="fa-solid fa-pen-to-square" size="2x" />
                                      </a>&nbsp;&nbsp;&nbsp;
                                      <a href="#" @click = "deletePurchase(purchase.object_uuid);" style="color: #373c59;">
                                        <font-awesome-icon icon="fa-solid fa-trash" size="2x" />
                                      </a>
                                    </td>
                                  </tr>
                                </template>
                              </template>
                            </template>

                          </template>
                        </template>
                      </template>
                    </template>
                  </template>
                  <tr v-if="(MaxRecsPage == false) && (NewRec == false) && (EditRec == false)">
                    <td colspan="25">
                      <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                              type="button"
                              @click="getRecs();">
                        Показать еще</button>
                    </td>
                  </tr>
                  </tbody>
                </table>
              </form>
            </div>
          </div>
        </div>

      </template>

    </TablesGrid>

  </div>

  <ModalAdmin v-show="showModal" @close-modal="showModal = false">
    <template v-slot:main-info>

      <div v-if="findAccPerforms == true">
        <b style="color: #373c59;">Запись таблицы 14ФП для МО "{{ editAPMoName }}" на {{editAPYearStart}}-{{editAPYearEnd}} г.г.</b><br>
        <FindAccPerformersGrid>

          <template v-slot:ap-grid-officials>
            <b>Должностные лица</b>
            <table class="fl-table">
              <thead>
              <tr>
                <th>ФИО</th>
                <th>Должность</th>
                <th>Телефон</th>
                <th>Удалить</th>
              </tr>
              </thead>
              <tbody>
              <tr v-if="LoadOFRecs == true">
                <td colspan="4" style="margin: 0 auto;">
                  <img src="../../../../assets/gifs/load.gif">
                </td>
              </tr>
              <tr v-if="LoadOFRecs == false" v-for="official in listOFRecs">
                <td>
                  {{ official.surname }} {{ official.name }}
                  {{ official.patronymic }}
                </td>
                <td>
                  {{ official.post }}
                </td>
                <td>
                  {{ official.phone }}
                </td>
                <td>
                  <a href="#" @click = "deleteOfficial(official.object_uuid);" style="color: #373c59;">
                    <font-awesome-icon icon="fa-solid fa-trash" />
                  </a>
                </td>
              </tr>
              </tbody>
            </table>
          </template>

          <template v-slot:ap-grid-contact-persons>
            <b>Контактные лица</b>
            <table class="fl-table">
              <thead>
              <tr>
                <th>ФИО</th>
                <th>Телефон</th>
                <th>Удалить</th>
              </tr>
              </thead>
              <tbody>
              <tr v-if = "LoadCPRecs == true">
                <td colspan="3" style="margin: 0 auto;">
                  <img src="../../../../assets/gifs/load.gif">
                </td>
              </tr>
              <tr v-if="LoadCPRecs == false" v-for = "cp in listCPRecs">
                <td>
                  {{ cp.surname }} {{ cp.name }} {{ cp.patronymic }}
                </td>
                <td>
                  {{ cp.phone }}
                </td>
                <td>
                  <a href="#" @click = "deleteCP(cp.object_uuid);" style="color: #373c59;">
                    <font-awesome-icon icon="fa-solid fa-trash"/>
                  </a>
                </td>
              </tr>
              </tbody>
            </table>
          </template>

          <template v-slot:ap-grid-find-ap>
            <b>Добавление контактного/должностного лица</b>
            <form @submit.prevent="findAPRecs();">
              <table class="fl-table">
                <thead>
                <tr>
                  <th colspan="5">
                    Поиск
                  </th>
                </tr>
                </thead>
                <tbody>
                <tr>
                  <td>
                    <input type="text" class="form-control text-center"
                           v-model="findApSurname" placeholder="Фамилия">
                  </td>
                  <td>
                    <input type="text" class="form-control text-center"
                           v-model="findApName" placeholder="Имя">
                  </td>
                  <td>
                    <input type="text" class="form-control text-center"
                           v-model="findApPatronymic" placeholder="Отчество">
                  </td>
                  <td>
                    <input type="text" class="form-control text-center"
                           v-model="findApPost" placeholder="Должность">
                  </td>
                  <td>
                    <input type="text" class="form-control text-center"
                           v-mask="'+7 (###) ###-##-##'"
                           v-model="findApPhone" placeholder="Телефон">
                  </td>
                </tr>
                <tr>
                  <td colspan="5">
                    <button class="btn btn-lg btn-primary iohk-butt"
                            type="submit">
                      Поиск
                    </button>
                  </td>
                </tr>
                </tbody>
              </table>
            </form><br>
            <table class="fl-table">
              <thead>
              <tr>
                <th>ФИО</th>
                <th>Должность</th>
                <th>Телефон</th>
                <th>Добавить как должностное лицо</th>
                <th>Добавить как контактное лицо</th>
              </tr>
              </thead>
              <tbody>
              <tr v-if="LoadFindAPRecs == true">
                <td colspan="5" style="margin: 0 auto;">
                  <img src="../../../../assets/gifs/load.gif">
                </td>
              </tr>
              <tr v-if="(listFindAPRecs.length == 0)  &&
                                    (LoadFindAPRecs == false)">
                <td colspan="5" style="margin: 0 auto;">
                  <b>Ничего не найдено</b>
                </td>
              </tr>
              <tr v-if="LoadFindAPRecs == false" v-for="ap in listFindAPRecs">
                <td>
                  {{ ap.surname }} {{ ap.name }} {{ ap.patronymic }}
                </td>
                <td>{{ ap.post }}</td>
                <td>{{ ap.phone }}</td>
                <td>
                  <div v-if="!(checkAPInOfficials(ap.object_uuid))">
                    <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                            type="button" @click="addOfficial(ap.object_uuid)">
                      <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>
                    </button>
                  </div>
                  <div v-if="checkAPInOfficials(ap.object_uuid)">
                    Добавлен
                  </div>
                </td>
                <td>
                  <div v-if="!(checkAPInCp(ap.object_uuid))">
                    <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                            type="button" @click="addCP(ap.object_uuid);">
                      <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>
                    </button>
                  </div>
                  <div v-if="checkAPInCp(ap.object_uuid)">
                    Добавлен
                  </div>
                </td>
              </tr>
              </tbody>
            </table>
          </template>

        </FindAccPerformersGrid>

      </div>

      <div v-if="tablesChoice == true">

        <TableChoice />

      </div>

      <div v-if="newMoDocsModal == true">

        <b>Выбор документа МО при создании/редактировании записи</b>
        <br>
        <table class="fl-table" style="width: 75%;">
          <thead>
          <tr>
            <th>
              Наименование документа <a href="javascript:void(0)">
              <div style="display: inline-block;" @click="sorted('mo_docs', 'name');">
                <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
              </div></a>
            </th>
            <th>
              Тип документа <a href="javascript:void(0)">
              <div style="display: inline-block;" @click="sorted('mo_docs', 'doc_type');">
                <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
              </div></a>
            </th>
            <th>
              Номер документа <a href="javascript:void(0)">
              <div style="display: inline-block;" @click="sorted('mo_docs', 'doc_number');">
                <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
              </div></a>
            </th>
            <th>
              Дата документа <a href="javascript:void(0)">
              <div style="display: inline-block;" @click="sorted('mo_docs', 'doc_date');">
                <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
              </div></a>
            </th>
            <th>Выбор документа</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="mo_doc in listNewMoDocs">
            <td>
              <a href="#" v-on:click="showDoc(mo_doc.doc_id, 'mo');">
                {{ mo_doc.name }}
              </a>
            </td>
            <td>{{ mo_doc.doc_kind }}</td>
            <td>{{ mo_doc.doc_number }}</td>
            <td>{{ mo_doc.doc_date }}</td>
            <td>
              <div v-if="NewRec == true">
                <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                        type="button" @click="setMoDoc('new', mo_doc.doc_id);">
                  Выбрать
                </button>
              </div>
              <div v-if="EditRec == true">
                <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                        type="button" @click="setMoDoc('edit', mo_doc.doc_id);">
                  Выбрать
                </button>
              </div>
            </td>
          </tr>
          </tbody>
        </table>

      </div>

      <div v-if="newOoDocsModal == true">

        <b>Выбор контракта ОО при создании новой записи в таблицу 14ФП</b>
        <br>
        <table class="fl-table" style="width: 75%;">
          <thead>
          <tr>
            <th>
              Наименование контракта <a href="javascript:void(0)">
              <div style="display: inline-block;" @click="sorted('oo_docs', 'doc_name');">
                <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
              </div></a>
            </th>
            <th>
              Номер контракта <a href="javascript:void(0)">
              <div style="display: inline-block;" @click="sorted('oo_docs', 'doc_number');">
                <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
              </div></a>
            </th>
            <th>
              Дата контракта <a href="javascript:void(0)">
              <div style="display: inline-block;" @click="sorted('oo_docs', 'doc_date');">
                <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
              </div></a>
            </th>
            <th>Выбор документа</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="doc in listNewOoDocs">
            <td>
              <a href="#" v-on:click="showDoc(doc.object_uuid, 'regular');">
                {{ doc.doc_name }}
              </a>
            </td>
            <td>{{ doc.doc_number }}</td>
            <td>{{ doc.doc_date }}</td>
            <td>
              <div v-if="NewRec == true">
                <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                        type="button" @click="setContract('new', doc.object_uuid);">
                  Выбрать
                </button>
              </div>
              <div v-if="EditRec == true">
                <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                        type="button" @click="setContract('edit', doc.object_uuid);">
                  Выбрать
                </button>
              </div>
            </td>
          </tr>
          </tbody>
        </table>

      </div>

      <div v-if="versionsRecModal == true">
        <b>Просмотр изменений закупки/контракта</b>
        <div class="special-table-wrapper">
          <table class="special-fl-table">
            <thead>
            <tr>
              <th>Дата изменения</th>
              <th>Документ-основание<br>дл изменения</th>
              <th>Мероприятие</th>
              <th>Размер субсидий ({{ versionsYearStart }} г.)<br> на мероприятие , рублей</th>
              <th>Размер субсидий ({{ versionsYearEnd }} г.)<br> на мероприятие , рублей</th>
              <th>Дата объявления закупки</th>
              <th>Ссылка на закупку</th>
              <th>Дата проведения аукциона</th>
              <th>Подрядчик/Поставщик,<br> дата, номер контракта</th>
              <th>Цена контракта, рублей</th>
              <th>Заказчик</th>
              <th>Дата заключения контракта/<br> или планируемая дата</th>
              <th>Дата окончания контракта</th>
              <th>Комментарий по проведенным<br> переговорам с потенциальными подрядчиками</th>
              <th>Дата начала работ на объекте</th>
              <th>Перерасчет сметной стоимости КР</th>
              <th>Портал актуальной информации<br> о ходе ремонтных работ</th>
            </tr>
            </thead>
            <tbody>
            <tr>
              <td>{{ format(recParent.created_at)}}</td>
              <td>
                <a href="#" @click="showDoc(recParent.mo_doc_id, 'mo');">
                  {{ recParent.mo_doc_kind }} № {{ recParent.mo_doc_number }}
                  от {{ format(recParent.mo_doc_date) }} г.
                </a>
              </td>
              <td>{{ recParent.event_name }}</td>
              <td style="white-space: nowrap;" colspan="2">
                {{ String(recParent.event_grant_start.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
              </td>
              <td style="white-space: nowrap;">
                {{ String(recParent.event_grant_end.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
              </td>
              <td>
                <div v-if="recParent.date_announce != null">
                  {{ format(recParent.date_announce) }}
                </div>
                <div v-if="recParent.date_announce == null">
                  -
                </div>
              </td>
              <td>
                <div v-if="checkUrl(recParent.url_purchase)">
                  <a :href="recParent.url_purchase" target="_blank">
                    {{ recParent.url_purchase }}
                  </a>
                </div>
                <div v-if="!(checkUrl(recParent.url_purchase))">
                  {{ recParent.url_purchase }}
                </div>
              </td>
              <td>
                <div v-if="recParent.date_auction != null">
                  {{ format(recParent.date_auction) }}
                </div>
                <div v-if="recParent.date_auction == null">
                  -
                </div>
              </td>
              <td>
                <div v-if="recParent.contract_id != null">
                  <a href="#" @click="showDoc(recParent.contract_id, 'regular');">
                    {{ recParent.provider_and_contract_info }}
                  </a>
                </div>
                <div v-if="recParent.contract_id == null">
                  {{ recParent.provider_and_contract_info }}
                </div>
              </td>
              <td style="white-space: nowrap;">
                {{ String(recParent.contract_price.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
              </td>
              <td>
                {{ recParent.customer }}
              </td>
              <td>
                <div v-if="recParent.date_contract_start != null">
                  {{ format(recParent.date_contract_start) }}
                </div>
                <div v-if="recParent.date_contract_start == null">
                  -
                </div>
              </td>
              <td>
                <div v-if="recParent.date_contract_end != null">
                  {{ format(recParent.date_contract_end) }}
                </div>
                <div v-if="recParent.date_contract_end == null">
                  -
                </div>
              </td>
              <td>
                {{ recParent.comment }}
              </td>
              <td>
                <div v-if="recParent.date_work_start != null">
                  {{ format(recParent.date_work_start) }}
                </div>
                <div v-if="recParent.date_work_start == null">
                  -
                </div>
              </td>
              <td>
                <div v-if="recParent.recalc == true">
                  <b>Да</b>
                </div>
                <div v-if="recParent.recalc == false">
                  <b>Нет</b>
                </div>
              </td>
              <td>
                <a :href="recParent.portal"
                   target="_blank">
                  {{ recParent.portal }}
                </a>
              </td>
            </tr>
            <tr v-for=" rec in listChanges">
              <td>{{ format(rec.created_at)}}</td>
              <td>
                <a href="#" @click="showDoc(rec.mo_doc_id, 'mo');">
                  {{ rec.mo_doc_kind }} № {{ rec.mo_doc_number }}
                  от {{ format(rec.mo_doc_date) }} г.
                </a>
              </td>
              <td>{{ rec.event_name }}</td>
              <td style="white-space: nowrap;" colspan="2">
                {{ String(rec.event_grant_start.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
              </td>
              <td style="white-space: nowrap;">
                {{ String(rec.event_grant_end.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
              </td>
              <td>
                <div v-if="rec.date_announce != null">
                  {{ format(rec.date_announce) }}
                </div>
                <div v-if="rec.date_announce == null">
                  -
                </div>
              </td>
              <td>
                <div v-if="checkUrl(rec.url_purchase)">
                  <a :href="rec.url_purchase" target="_blank">
                    {{ rec.url_purchase }}
                  </a>
                </div>
                <div v-if="!(checkUrl(rec.url_purchase))">
                  {{ rec.url_purchase }}
                </div>
              </td>
              <td>
                <div v-if="rec.date_auction != null">
                  {{ format(rec.date_auction) }}
                </div>
                <div v-if="rec.date_auction == null">
                  -
                </div>
              </td>
              <td>
                <div v-if="rec.contract_id != null">
                  <a href="#" @click="showDoc(rec.contract_id, 'regular');">
                    {{ rec.provider_and_contract_info }}
                  </a>
                </div>
                <div v-if="rec.contract_id == null">
                  {{ rec.provider_and_contract_info }}
                </div>
              </td>
              <td style="white-space: nowrap;">
                {{ String(rec.contract_price.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ") }}
              </td>
              <td>
                {{ rec.customer }}
              </td>
              <td>
                <div v-if="rec.date_contract_start != null">
                  {{ format(rec.date_contract_start) }}
                </div>
                <div v-if="rec.date_contract_start == null">
                  -
                </div>
              </td>
              <td>
                <div v-if="rec.date_contract_end != null">
                  {{ format(rec.date_contract_end) }}
                </div>
                <div v-if="rec.date_contract_end == null">
                  -
                </div>
              </td>
              <td>
                {{ rec.comment }}
              </td>
              <td>
                <div v-if="rec.date_work_start != null">
                  {{ format(rec.date_work_start) }}
                </div>
                <div v-if="rec.date_work_start == null">
                  -
                </div>
              </td>
              <td>
                <div v-if="rec.recalc == true">
                  <b>Да</b>
                </div>
                <div v-if="rec.recalc == false">
                  <b>Нет</b>
                </div>
              </td>
              <td>
                <a :href="rec.portal"
                   target="_blank">
                  {{ rec.portal }}
                </a>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>

    </template>
  </ModalAdmin>

  <SideBox>

    <template v-slot:side-chb>
      <input type="checkbox" id="side-checkbox" v-model="SideBoxChecked"/>
    </template>

    <template v-slot:sidebox-title>
      <p v-bind:class="[FindClass]">Поиск записей</p>
      <p v-bind:class="[AddClass]">Добавление записи</p>
      <p v-bind:class="[PeriodsClass]">Выбор периодов</p>
      <p v-bind:class="[FilterClass]">Филтрация по полю "{{displayFilterName}}"</p>
    </template>

    <template v-slot:main-table-trs>
      <tr v-if="PeriodsClass === 'sidebox-active'" v-for="period in listPeriods">
        <td style="width: 75%; text-align: center">{{period}}</td>
        <td style="text-align: center"><input type="checkbox" name="periodsCheckbox" :id="period" :checked="selectedPeriods.includes(period)" /></td>
      </tr>
      <tr v-if="FindClass == 'sidebox-active'">
        <td style="text-align: center;"><b>МО:</b></td>
        <td>
          <select class="form-control"
                  v-model="findMo">
            <option></option>
            <option v-for="mo in listMos">
              {{ mo.name }}
            </option>
          </select>
        </td>
      </tr>
      <tr v-if="AddClass === 'sidebox-active'">
        <td style="text-align: center;"><b>МО:</b></td>
        <td>
          <select class="form-control"
                  v-model="addMo">
            <option></option>
            <option v-for="mo in listMos">
              {{ mo.name }}
            </option>
          </select>
        </td>
      </tr>
      <tr v-if="AddClass === 'sidebox-active'">
        <td style="text-align: center;"><b>Год начала реализации:</b></td>
        <td>
          <input type="text" v-mask="'####'" class="form-control text-center" v-model="addYearStart">
        </td>
      </tr>
      <tr v-if="AddClass === 'sidebox-active'">
        <td style="text-align: center;"><b>Год окончания реализации:</b></td>
        <td>
          <input type="text" v-mask="'####'" class="form-control text-center" v-model="addYearEnd">
        </td>
      </tr>
      <tr v-if="FindClass == 'sidebox-active'">
        <td style="text-align: center;"><b>Год начала реализации:</b></td>
        <td>
          <input type="text" v-mask="'####'" class="form-control text-center" v-model="findYearStart">
        </td>
      </tr>
      <tr v-if="FindClass == 'sidebox-active'">
        <td style="text-align: center;"><b>Год окончания реализации:</b></td>
        <td>
          <input type="text" v-mask="'####'" class="form-control text-center" v-model="findYearEnd">
        </td>
      </tr>
      <tr v-if="FindClass == 'sidebox-active'">
        <td style="text-align: center;"><b>Полное наименование объекта КР:</b></td>
        <td>
          <textarea class="form-control mini-font" v-model="findOoShortName"></textarea>
        </td>
      </tr>
      <tr v-if="FindClass == 'sidebox-active'">
        <td style="text-align: center;"><b>Адрес объекта КР:</b></td>
        <td>
          <textarea class="form-control mini-font" v-model="findOoAddress"></textarea>
        </td>
      </tr>
      <tr v-if="FilterClass == 'sidebox-active'">
        <td style="text-align: center; vertical-align: top">
          <a href="#" @click="filterReset()">Сброс фильтров</a><br/>
          <b>Поиск:</b><br/>
          <div v-if="selectedFilter.includes('date')">
            <i>(В формате: гггг-мм-дд)</i><br/>
          </div>
          <div v-if="selectedFilter === 'contract_price'">
            <i>(Без пробелов-раздетилетей)</i><br/>
          </div>
          <input :value="findAllValues" @change="e => findAllValues = e.target.value" />
        </td>
        <td>
          <br/>
          <table style="border: 1">
            <template v-for="value in tableFilters[selectedFilter].allValues">
              <tr v-if="(findAllValues === null) || (String(value).includes(findAllValues))">
                <td>
                  {{
                    selectedFilter.includes('date') ?
                      format(value)
                      :
                      typeof value === 'number' ?
                        String(value.toFixed(2)).replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1 ')
                        :
                        value
                  }}&nbsp;&nbsp;&nbsp;
                </td>
                <td>
                  <input type="checkbox"
                         :name="'filter_'+selectedFilter"
                         @change="addOrDeleteValueToFilter(value)"
                         :checked="tableFilters[selectedFilter].selectedValues.includes(value)" />
                </td>
              </tr>
            </template>
          </table>
        </td>
      </tr>
    </template>

    <template v-slot:sidebox-button>
      <div id="main-content">
        <div v-if="FindClass === 'sidebox-active'">
          <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', FindClass]"
                  type="button" @click="findRecs();">
            Поиск
          </button>
        </div>
        <div v-if="AddClass === 'sidebox-active'">
          <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', AddClass]"
                  type="button" @click="add14FPRec();">
            Добавить
          </button>
        </div>
        <div v-if="PeriodsClass === 'sidebox-active'">
          <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', PeriodsClass]"
                  type="button" @click="changePeriods();">
            Выбрать
          </button>
        </div>
        <div v-if="FilterClass === 'sidebox-active'">
          <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', FilterClass]"
                  type="button" @click="filterRecs();">
            Применить
          </button>
        </div>
      </div>
    </template>

  </SideBox>

</template>

<script>
import Header from "../../../../components/Header.vue"
import SideBox from "../../../../components/SideBox.vue"
import TablesGrid from "../../../../components/grids/TablesGrid.vue"
import FindAccPerformersGrid from "../../../../components/grids/FindAccPerformersGrid.vue"
import ModalAdmin from '../../../../components/modals/ModalAdmin.vue'
import TableChoice from '../../../../components/menus/TablesChoice.vue'

export default {
  name: "WK14FP",
  components: {
    Header,
    SideBox,
    TablesGrid,
    FindAccPerformersGrid,
    ModalAdmin,
    TableChoice
  },
  data() {
    return {
      downloadLoad: false,
      ContractPriceTooMuch: false,
      sortedbyASC: true,
      oneYearPeriod: false,
      oneYearSubsidy: false,
      SideBoxChecked: false,
      tablesChoice: true,
      DetailClass:'sidebox-deactive',
      FindClass:'sidebox-deactive',
      AddClass:'sidebox-deactive',
      FilterClass: 'sidebox-deactive',

      fieldsList: [
        {
          field: 'event_name',
          alias: 'Мероприятие'
        },
        {
          field: 'date_announce',
          alias: 'Дата объявления закупки'
        },
        {
          field: 'url_purchase',
          alias: 'Ссылка на закупку'
        },
        {
          field: 'date_auction',
          alias: 'Дата проведения аукциона'
        },
        {
          field: 'provider_and_contract_info',
          alias: 'Подрядчик/Поставщик, дата, номер контракта'
        },
        {
          field: 'contract_price',
          alias: 'Цена контракта'
        },
        {
          field: 'date_contract_start',
          alias: 'Дата заключения контракта/планируемая дата'
        },
        {
          field: 'date_contract_end',
          alias: 'Дата окончания контракта'
        },
        {
          field: 'comment',
          alias: 'Комментарий по переговорам'
        },
        {
          field: 'date_work_start',
          alias: 'Дата начала работ/поставки'
        },
        {
          field: 'recalc',
          alias: 'Перерасчет сметной стоимости КР'
        },
        {
          field: 'portal',
          alias: 'Портал актуальной информации'
        }
      ],
      findAllValues: '',
      tableFilters: {
        event_name: {
          allValues: [],
          selectedValues: []
        },
        date_announce: {
          allValues: [],
          selectedValues: []
        },
        url_purchase: {
          allValues: [],
          selectedValues: []
        },
        date_auction: {
          allValues: [],
          selectedValues: []
        },
        provider_and_contract_info: {
          allValues: [],
          selectedValues: []
        },
        contract_price: {
          allValues: [],
          selectedValues: []
        },
        date_contract_start: {
          allValues: [],
          selectedValues: []
        },
        date_contract_end: {
          allValues: [],
          selectedValues: []
        },
        comment: {
          allValues: [],
          selectedValues: []
        },
        date_work_start: {
          allValues: [],
          selectedValues: []
        },
        recalc: {
          allValues: [],
          selectedValues: []
        },
        portal: {
          allValues: [],
          selectedValues: []
        }
      },
      selectedFilter: '',
      displayFilterName: '',

      money: {
        decimal: '.',
        thousands: ' ',
        prefix: '',
        suffix: '',
        precision: 2,
        masked: true
      },

      LoadClass: 'vue-active',
      ContentClass: 'vue-deactive',

      counter: 0,

      sourceRecs: [],
      listRecs: [],
      listOFRecs: [],
      listCPRecs: [],
      listFindAPRecs: [],
      listNewMoDocs: [],
      listNewOoDocs: [],
      listChanges: [],
      recParent: [],
      listMos: [],
      SubsidyInfo: [],

      listEvents: [],
      listPeriods: [],
      detailRec: [],
      selectedOoShortName: '(не выбрано)',
      selectedOoCapacity: 0,
      selectedOoAddress: '',

      findString: '',
      findAPString: '',

      recs_page: 1,
      MaxRecsPage: false,

      editRecCounter: 0,

      NewRec: false,
      newRecSubsidyLoad: false,
      newRecArr: [],
      newRecEventSelect: '',
      newRecObjectUuid: '',
      newRecMoDocUuid: null,
      newRecMoDoc: '',
      newMoDocsModal: false,
      newRecOoDocUuid: '',
      newOoDocsModal: false,
      newRecMinObrMOUuid: '',
      newRecTotalYearStart: 0.0,
      newRecTotalYearEnd: 0.0,
      newRecProviderInfo: '',
      newRecContractPrice: 0.0,
      newRecRecalc: false,

      EditRec: false,
      editRecSubsidyLoad: false,
      editRecArr: [],
      editRecEventSelect: '',
      editRecPurchaseUuid: '',
      editRecObjectUuid: '',
      editRecMoDocUuid: null,
      editRecMoDoc: '',
      editMoDocsModal: false,
      editRecOoDocUuid: '',
      editOoDocsModal: false,
      editRecMinObrMOUuid: '',
      editRecTotalYearStart: 0.0,
      editRecTotalYearEnd: 0.0,
      editRecProviderInfo: '',
      editRecContractPrice: 0.0,
      editRecRecalc: false,

      editRecDateAnnounce: '',
      editRecUrlPurchase: '',
      editRecDateAuction: '',
      editRecOoDocUuid: '',
      editRecProviderInfo: '',
      editRecContractPrice: 0.0,
      editRecCustomer: '',
      editRecDateContractStart: '',
      editRecDateContractEnd: '',
      editRecComment: '',
      editRecDateWorkStart: '',
      editRecRecalc: false,
      editRecPortal: '',

      findAccPerforms: false,
      findMo: '',
      addMo: '',
      addYearStart: '',
      addYearEnd: '',

      editAPUuid: '',
      editAPMoName: '',
      editAPYearStart: '',
      editAPYearEnd: '',

      apNotFound: false,

      versionsRecModal: false,
      versionsYearStart: 0,
      versionsYearEnd: 0,

      editReccUuid: '',

      showModal: false,
      showOoFindResults: false,
      ooNotFound: false,
      showFindButton: true,

      LoadRecs: true,
      LoadOFRecs: true,
      LoadCPRecs: true,
      LoadFindAPRecs: false,
      selectPeriod: 'Все',

      PeriodsClass: 'sidebox-deactive',
      selectedPeriods: []

    }
  },
  methods: {
    checkOneYearPeriod() {
      if ((this.selectPeriod == 'Все' &&
        (this.newYearStart != this.newYearEnd || this.editYearStart != this.editYearEnd)) || (this.selectPeriod != 'Все' &&
        this.getYearStartFromPeriod(this.selectPeriod) != this.getYearEndFromPeriod(this.selectPeriod))) {
        this.oneYearPeriod = false
      } else {
        this.oneYearPeriod = true
      }
    },
    sorted(type, field){
      switch(type){
        case 'mo_docs':
          if (this.sortedbyASC) {
            if(field.includes('date')){
              this.listNewMoDocs.sort((x, y) => (this.convertStrDate(x[field]) > this.convertStrDate(y[field]) ? -1 : 1))
            } else {
              this.listNewMoDocs.sort((x, y) => (x[field] > y[field] ? -1 : 1));
            }
            this.sortedbyASC = false;
          } else {
            if(field.includes('date')){
              this.listNewMoDocs.sort((x, y) => (this.convertStrDate(x[field]) < this.convertStrDate(y[field]) ? -1 : 1))
            } else {
              this.listNewMoDocs.sort((x, y) => (x[field] < y[field] ? -1 : 1));
            }
            this.sortedbyASC = true;
          }
          break

        case 'oo_docs':
          if (this.sortedbyASC) {
            if(field.includes('date')){
              this.listNewOoDocs.sort((x, y) => (this.convertStrDate(x[field]) > this.convertStrDate(y[field]) ? -1 : 1))
            } else {
              this.listNewOoDocs.sort((x, y) => (x[field] > y[field] ? -1 : 1));
            }
            this.sortedbyASC = false;
          } else {
            if(field.includes('date')){
              this.listNewOoDocs.sort((x, y) => (this.convertStrDate(x[field]) < this.convertStrDate(y[field]) ? -1 : 1))
            } else {
              this.listNewOoDocs.sort((x, y) => (x[field] < y[field] ? -1 : 1));
            }
            this.sortedbyASC = true;
          }
          break
      }

    },
    editAPAction(uuid) {
      this.editAPUuid=uuid
      for (let i=0;i<this.listRecs.length;i++){
        if(this.listRecs[i].object_uuid == uuid) {
          let rec = this.listRecs[i]
          this.editAPMoName = rec.mo_name
          this.editAPYearStart = rec.year_start
          this.editAPYearEnd = rec.year_end
          break;
        }
      }
      this.getOfRecs()
      this.getCPRecs()
      this.showModalAction('findAP')

    },
    showModalAction(action) {
      switch(action){
        case "tables":
          this.findAccPerforms = false
          this.newMoDocsModal = false
          this.newOoDocsModal = false
          this.tablesChoice = true
          this.versionsRecModal = false
          break;
        case "findAP":
          this.findAccPerforms = true
          this.newMoDocsModal = false
          this.newOoDocsModal = false
          this.tablesChoice = false
          this.versionsRecModal = false
          break;
        case "newMoDoc":
          this.findAccPerforms = false
          this.newMoDocsModal = true
          this.newOoDocsModal = false
          this.tablesChoice = false
          this.versionsRecModal = false
          break;
        case "newOoDoc":
          this.findAccPerforms = false
          this.newMoDocsModal = false
          this.newOoDocsModal = true
          this.tablesChoice = false
          this.versionsRecModal = false
          break;
        case "versionsRec":
          this.findAccPerforms = false
          this.newMoDocsModal = false
          this.newOoDocsModal = false
          this.tablesChoice = false
          this.versionsRecModal = true
          break;
      }
      this.showModal = true
    },
    getRowsSpanMo(uuid) {
      let total_count = 0
      for(let i=0;i<this.listRecs.length;i++){
        if (this.listRecs[i].object_uuid == uuid) {
          if(this.listRecs[i].objects.length != 0) {
            let objects = this.listRecs[i].objects
            for(let j=0;j<objects.length;j++){
              if(objects[j].purchases.length != 0){
                total_count += objects[j].purchases.length
              } else {
                total_count++
              }
            }
          } else {
            total_count++
          }
        }
      }
      return total_count
    },
    getRowsSpanObject(rec_uuid, obj_uuid) {
      let total_count = 0
      for(let i=0;i<this.listRecs.length;i++){
        if (this.listRecs[i].object_uuid == rec_uuid) {
          let objects = this.listRecs[i].objects
          for(let j=0;j<objects.length;j++){
            if(objects[j].object_uuid == obj_uuid){
              if(objects[j].purchases.length != 0) {
                let purchases = objects[j].purchases
                total_count += objects[j].purchases.length
              } else {
                total_count++
                break;
              }
            }
          }
        }
      }
      return total_count
    },
    getMoDocsInfo(mo_uuid) {
      let info=[]
      let check_exist = true
      let doc_info=[]
      let mo_doc_info = ''
      let mo_doc_uuid = ''
      for(let i=0;i<this.listRecs.length;i++){
        if (this.listRecs[i].object_uuid == mo_uuid) {
          if(this.listRecs[i].objects != null) {
            let objects = this.listRecs[i].objects
            for(let j=0;j<objects.length;j++) {
              if(objects[j].purchases != null) {
                let purchases = objects[j].purchases
                check_exist = false
                for(let k=0;k<purchases.length;k++) {
                  doc_info = []
                  mo_doc_uuid = purchases[k].mo_doc_id
                  for (let k=0;k<info.length;k++) {
                    if (info[k][0] == mo_doc_uuid) {
                      check_exist = true
                      break
                    }
                  }
                  if (check_exist == false) {
                    mo_doc_info  = purchases[k].mo_doc_kind+' №'+purchases[k].mo_doc_number
                      +' от '+convertDateToStr(purchases[k].mo_doc_date)
                    doc_info.push(mo_doc_uuid)
                    doc_info.push(mo_doc_info)
                    info.push(doc_info)
                  }
                }
              } else {
                break;
              }
            }
          } else {
            break;
          }
        }
      }
      return info
    },
    showEditForm(purchase_uuid, rec_uuid, obj_uuid, mo_uuid) {
      this.getMoDocs(mo_uuid)
      this.NewRec = false
      this.editRecArr.length = 0
      this.editRecObjectUuid = obj_uuid
      this.editRecPurchaseUuid = purchase_uuid
      for(let i=0;i<this.listRecs.length;i++){
        if(this.listRecs[i].object_uuid == rec_uuid) {
          if (this.listRecs[i].year_start == this.listRecs[i].year_end) {
            this.oneYearSubsidy = true
          } else {
            this.oneYearSubsidy = false
          }
          this.editRecArr.push(this.listRecs[i].year_start)
          this.editRecArr.push(this.listRecs[i].year_end)
          this.editRecArr.push(this.listRecs[i].mo_name)
          for(let j=0;j<this.listRecs[i].objects.length;j++) {
            if(this.listRecs[i].objects[j].object_uuid == obj_uuid) {
              this.editRecMinObrMOUuid = this.listRecs[i].objects[j].minobrmo_uuid
              this.editRecArr.push(this.listRecs[i].objects[j].oo_fullname)
              for(let k=0;k<this.listRecs[i].objects[j].purchases.length;k++) {
                if(this.listRecs[i].objects[j].purchases[k].object_uuid == purchase_uuid) {
                  let purchase = this.listRecs[i].objects[j].purchases[k]
                  for (let h=0;h<this.listEvents.length;h++){
                    if(this.listEvents[h].full_name == purchase.event_name) {
                      this.editRecEventSelect = this.listEvents[h].uuid
                      break
                    }
                  }
                  this.editRecTotalYearStart = purchase.event_grant_start.toFixed(2)
                  this.editRecTotalYearEnd = purchase.event_grant_end.toFixed(2)
                  this.editRecDateAnnounce = purchase.date_announce
                  this.editRecUrlPurchase = purchase.url_purchase
                  this.editRecDateAuction = purchase.date_auction
                  this.editRecOoDocUuid = purchase.contract_id
                  this.editRecProviderInfo = purchase.provider_and_contract_info
                  this.editRecContractPrice = purchase.contract_price.toFixed(2)
                  this.editRecCustomer = purchase.customer
                  this.editRecDateContractStart = purchase.date_contract_start
                  this.editRecDateContractEnd = purchase.date_contract_end
                  this.editRecComment = purchase.comment
                  this.editRecDateWorkStart = purchase.date_work_start
                  this.editRecRecalc = purchase.recalc
                  this.editRecPortal = purchase.portal
                  break
                }
              }
              break
            }
          }
          break
        }
      }
      this.getOoDocs(this.editRecMinObrMOUuid)
      this.EditRec = true
      ResizeTables()
    },
    async updatePurchase() {
      if ((this.editRecMoDocUuid == null) || (this.editRecMoDocUuid.length == 0)) {
        showBanner('.banner.error', 'Выберите документ МО')
        return false
      }
      if ((this.editRecEventSelect.length == 0) || (this.editRecEventSelect == null)) {
        showBanner('.banner.error', 'Выберите мероприятие')
        return false
      }
      if (!(isValidHttpUrl(this.editRecPortal))) {
        showBanner('.banner.error', 'Введеная строка в поле "Портал актуальной'
          +'информации о ходе ремонтных работ" не является корректным URL адресом')
        return false
      }
      this.EditRec = false
      this.LoadRecs = true
      this.listRecs = []
      this.recs_page = 1
      this.MaxRecsPage = false
      let data = new FormData()
      data.append('purchase_uuid', this.editRecPurchaseUuid)
      data.append('event_id', this.editRecEventSelect)
      data.append('mo_doc_id', this.editRecMoDocUuid)
      data.append('event_grant_end', this.convertMoneyToNumber(this.editRecTotalYearEnd))
      if (!(this.oneYearSubsidy)) {
        data.append('event_grant_start', this.convertMoneyToNumber(this.editRecTotalYearStart))
      } else {
        data.append('event_grant_start', '0.00')
      }
      data.append('date_announce', this.editRecDateAnnounce)
      data.append('url_purchase', this.editRecUrlPurchase)
      data.append('date_auction', this.editRecDateAuction)
      if ((this.editRecOoDocUuid == null) || (this.editRecOoDocUuid.length == 0)) {
        data.append('contract_id', null)
      } else {
        data.append('contract_id', this.editRecOoDocUuid)
      }
      data.append('provider_and_contract_info', this.editRecProviderInfo)
      data.append('contract_price', this.convertMoneyToNumber(this.editRecContractPrice))
      data.append('customer', this.editRecCustomer)
      data.append('date_contract_start', this.editRecDateContractStart)
      data.append('date_contract_end', this.editRecDateContractEnd)
      data.append('comment', this.editRecComment)
      data.append('date_work_start', this.editRecDateWorkStart)
      data.append('recalc', this.editRecRecalc)
      data.append('portal', this.editRecPortal)
      await fetch(this.$store.state.backendUrl+'/api/v1/admin/tables/purchasewk14fp/'+this.editRecObjectUuid+'/', {
        method: 'put',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Authorization': 'Token '+localStorage.getItem('access_token')
        },
        body: data
      })
        .then(resp => { return resp.json()})
        .then(data => {
          if (data.success) {
            showBanner('.banner.success', data['success'])
          } else {
            showBanner('.banner.error', data['error'])
            return false
          }
        })
      this.getRecs()
    },
    showNewRec(rec_uuid, obj_uuid, mo_uuid) {
      this.EditRec = false
      this.newRecArr.length = 0
      this.newRecObjectUuid = obj_uuid
      for(let i=0;i<this.listRecs.length;i++){
        if(this.listRecs[i].object_uuid == rec_uuid) {
          if (this.listRecs[i].year_start == this.listRecs[i].year_end) {
            this.oneYearSubsidy = true
          } else {
            this.oneYearSubsidy = false
          }
          this.newRecArr.push(this.listRecs[i].year_start)
          this.newRecArr.push(this.listRecs[i].year_end)
          this.newRecArr.push(this.listRecs[i].mo_name)
          for(let j=0;j<this.listRecs[i].objects.length;j++) {
            if(this.listRecs[i].objects[j].object_uuid == obj_uuid) {
              this.newRecMinObrMOUuid = this.listRecs[i].objects[j].minobrmo_uuid
              this.newRecArr.push(this.listRecs[i].objects[j].oo_fullname)
              break
            }
          }
          break
        }
      }
      this.newRecEventSelect = ''
      this.newRecMoDocUuid = null
      this.newRecTotalYearStart = 0.0
      this.newRecTotalYearEnd = 0.0
      this.newRecDateAnnounce = null
      this.newRecUrlPurchase = null
      this.newRecDateAuction = null
      this.newRecOoDocUuid = null
      this.newRecProviderInfo = null
      this.newRecContractPrice = 0.0
      this.newRecCustomer = null
      this.newRecDateContractStart = null
      this.newRecDateContractEnd = null
      this.newRecComment = null
      this.newRecDateWorkStart = null
      this.newRecRecalc = false
      this.newRecPortal = null
      this.getMoDocs(mo_uuid)
      this.getOoDocs(this.newRecMinObrMOUuid)
      this.NewRec = true
      ResizeTables()
    },
    async getMoDocs(uuid) {
      let url = this.$store.state.backendUrl+'/api/v1/docs/get_mo_docs_wk14fp?mo_uuid='+uuid
      this.listNewMoDocs = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': 'Token '+localStorage.getItem('access_token'),
        },
      })
        .then(resp => { return resp.json() })
        .then(data => {
          if (data['error']) {
            showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
            return false
          } else {
            return data
          }
        })
    },
    setMoDoc(type, uuid) {
      for(let i=0;i<this.listNewMoDocs.length;i++){
        if(this.listNewMoDocs[i].doc_id == uuid){
          let rec = this.listNewMoDocs[i]
          if (type == 'new') {
            this.newRecMoDoc = rec.doc_kind+' № '+rec.doc_number+' от '+rec.doc_date+ ' г.'
            this.newRecMoDocUuid = uuid
          } else {
            this.editRecMoDoc = rec.doc_kind+' № '+rec.doc_number+' от '+rec.doc_date+ ' г.'
            this.editRecMoDocUuid = uuid
          }
          break;
        }
      }
      this.showModal = false
    },
    async getOoDocs(uuid) {
      let url = this.$store.state.backendUrl+'/api/v1/docs/get_oo_docs_wk14fp?minobrmo_uuid='+uuid
      this.listNewOoDocs = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': 'Token '+localStorage.getItem('access_token'),
        },
      })
        .then(resp => { return resp.json() })
        .then(data => {
          if (data['error']) {
            showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
            return false
          } else {
            return data
          }
        })
    },
    setContract(type,  uuid) {
      for(let i=0;i<this.listNewOoDocs.length;i++){
        if(this.listNewOoDocs[i].object_uuid == uuid){
          let rec = this.listNewOoDocs[i]
          if (type == 'new') {
            this.newRecProviderInfo = rec.provider+', № '+rec.doc_number+' от '+rec.doc_date+ ' г.'
            this.newRecContractPrice = rec.contract_price.toFixed(2)
            this.newRecOoDocUuid = uuid
          } else {
            this.editRecProviderInfo = rec.provider+', № '+rec.doc_number+' от '+rec.doc_date+ ' г.'
            this.editRecContractPrice = rec.contract_price.toFixed(2)
            this.editRecOoDocUuid = uuid
          }
          break;
        }
      }
      this.showModal = false
    },
    async showDoc(uuid, type) {
      await fetch(this.$store.state.backendUrl+'/api/v1/docs/show_doc/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'application/json;charset=UTF-8',
          'Authorization': 'Token '+localStorage.getItem('access_token')
        },
        body: JSON.stringify({
          'type_doc': type,
          'doc_uuid': uuid
        })
      })
        .then(response => {response.blob().then(blob => {
          let url = window.URL.createObjectURL(blob);
          if (blob['type'].includes('officedocument.wordprocessingml.document') ||
            blob['type'].includes('officedocument.spreadsheetml.sheet')) {
            let a = document.createElement("a");
            a.href = url;
            if (blob['type'].includes('officedocument.wordprocessingml.document')) {
              a.download = 'Контракт.docx';
            } else {
              a.download = 'Контракт.xlsx';
            }
            a.click();
          } else {
            window.open(url, '_blank').focus();
          }
        })
        })
    },
    async getSubsidyInfo(type) {
      let url = ''
      if (type == 'new') {
        this.newRecSubsidyLoad = true
        url = this.$store.state.backendUrl+'/api/v1/admin/wk14fp_get_subsidy_info?minobrmo_uuid='+
          this.newRecMinObrMOUuid+'&event_uuid='+this.newRecEventSelect
      } else {
        this.editRecSubsidyLoad = true
        url = this.$store.state.backendUrl+'/api/v1/admin/wk14fp_get_subsidy_info?minobrmo_uuid='+
          this.editRecMinObrMOUuid+'&event_uuid='+this.editRecEventSelect
      }
      await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': 'Token '+localStorage.getItem('access_token'),
        },
      })
        .then(resp => { return resp.json() })
        .then(data => {
          if (data['error']) {
            showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
            return false
          } else {
            if (type == 'new') {
              this.newRecTotalYearStart = data['year_start']
              this.newRecTotalYearEnd = data['year_end']
            } else {
              this.editRecTotalYearStart = data['year_start']
              this.editRecTotalYearEnd = data['year_end']
            }
            this.SubsidyInfo = data
            return true
          }
        })
      if (type == 'new') {
        this.newRecSubsidyLoad = false
      } else {
        this.editRecSubsidyLoad = false
      }
    },
    async newPurchase() {
      if ((this.newRecMoDocUuid == null) || (this.newRecMoDocUuid.length == 0)) {
        showBanner('.banner.error', 'Выберите документ МО')
        return false
      }
      if ((this.newRecEventSelect.length == 0) || (this.newRecEventSelect == null)) {
        showBanner('.banner.error', 'Выберите мероприятие')
        return false
      }
      this.NewRec = false
      this.LoadRecs = true
      this.listRecs = []
      this.recs_page = 1
      this.MaxRecsPage = false
      let data = new FormData()
      data.append('obj_uuid', this.newRecObjectUuid)
      data.append('event_id', this.newRecEventSelect)
      data.append('mo_doc_id', this.newRecMoDocUuid)
      data.append('event_grant_end', this.convertMoneyToNumber(this.newRecTotalYearEnd))
      if (!(this.oneYearSubsidy)) {
        data.append('event_grant_start', this.convertMoneyToNumber(this.newRecTotalYearStart))
      } else {
        data.append('event_grant_start', '0.00')
      }
      data.append('date_announce', this.newRecDateAnnounce)
      data.append('url_purchase', this.newRecUrlPurchase)
      data.append('date_auction', this.newRecDateAuction)
      if ((this.newRecOoDocUuid == null) || (this.newRecOoDocUuid.length == 0)) {
        data.append('contract_id', null)
      } else {
        data.append('contract_id', this.newRecOoDocUuid)
      }
      data.append('provider_and_contract_info', this.newRecProviderInfo)
      data.append('contract_price', this.convertMoneyToNumber(this.newRecContractPrice))
      data.append('customer', this.newRecCustomer)
      data.append('date_contract_start', this.newRecDateContractStart)
      data.append('date_contract_end', this.newRecDateContractEnd)
      data.append('comment', this.newRecComment)
      data.append('date_work_start', this.newRecDateWorkStart)
      data.append('recalc', this.newRecRecalc)
      data.append('portal', this.newRecPortal)
      await fetch(this.$store.state.backendUrl+'/api/v1/admin/tables/purchasewk14fp/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Authorization': 'Token '+localStorage.getItem('access_token')
        },
        body: data
      })
        .then(resp => { return resp.json()})
        .then(data => {
          if (data.success) {
            showBanner('.banner.success', data['success'])
          } else {
            showBanner('.banner.error', data['error'])
            return false
          }
        })
      this.getRecs()
      this.getPeriods()
    },
    showVersions(rec_uuid, obj_uuid, purchase_uuid) {
      for(let i=0;i<this.listRecs.length;i++){
        if(this.listRecs[i].object_uuid == rec_uuid) {
          this.versionsYearStart = this.listRecs[i].year_start
          this.versionsYearEnd = this.listRecs[i].year_end
          for(let j=0;j<this.listRecs[i].objects.length;j++) {
            if(this.listRecs[i].objects[j].object_uuid == obj_uuid) {
              let purchases = this.listRecs[i].objects[j].purchases
              for (let k=0;k<purchases.length;k++) {
                if (purchases[k].object_uuid ==  purchase_uuid) {
                  this.recParent = purchases[k]
                  this.listChanges = purchases[k].changes
                  break
                }
              }
              break;
            }
          }
          break;
        }
      }
      this.showModalAction('versionsRec')

    },
    convertMoneyToNumber(money) {
      if (money != null) {
        let str = money.trim()
        if (money.indexOf('.') != -1) {
          let no_space = str.split(' ').join('');
          str = no_space.replace(/[\s.,%]/g, '');
        }
        let first = str.substring(0, str.length-2);
        let end = str.substring(str.length-2);
        let final = first+'.'+end
        return final
      }
      return money
    },
    async getPeriods() {
      let url = this.$store.state.backendUrl+'/api/v1/admin/tables/mpsr/'
      let periods = []
      let results = []
      await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': 'Token '+localStorage.getItem('access_token'),
        },
      })
        .then(resp => { return resp.json() })
        .then(data => {
          if (data['error']) {
            if (this.recs_page == 1) {
              showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
              return false
            } else {
              showBanner('.banner.success', 'Отображены все записи')
              this.MaxRecsPage = true
              return false
            }
          }
          results = data
        })

      for (let i=0;i<results.length;i++) {
        periods.push(results[i].year_start+'-'+results[i].year_end)
        this.selectedPeriods.push(results[i].year_start+'-'+results[i].year_end)
      }
      this.listPeriods = [... new Set(periods)];
      this.listPeriods.sort((x, y) => (x > y ? -1 : 1))
    },
    async getOfRecs() {
      this.LoadOFRecs = true
      let url = this.$store.state.backendUrl+'/api/v1/admin/tables/ofwk14fp?wk14fp_uuid='+this.editAPUuid
      this.listOFRecs = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': 'Token '+localStorage.getItem('access_token'),
        },
      })
        .then(resp => { return resp.json() })
        .then(data => {
          if (data['error']) {
            showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
            return false
          } else {
            return data
          }
        })
      this.LoadOFRecs = false
    },
    async getCPRecs() {
      this.LoadCPRecs = true
      let url = this.$store.state.backendUrl+'/api/v1/admin/tables/cpwk14fp?wk14fp_uuid='+this.editAPUuid
      this.listCPRecs = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': 'Token '+localStorage.getItem('access_token'),
        },
      })
        .then(resp => { return resp.json() })
        .then(data => {
          if (data['error']) {
            showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
            return false
          } else {
            return data
          }
        })
      this.LoadCPRecs = false
    },
    async getFindAPRecs() {
      this.LoadFindAPRecs = true
      let url = this.$store.state.backendUrl+'/api/v1/admin/find_acc_performers?'+this.findAPString
      this.listFindAPRecs = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': 'Token '+localStorage.getItem('access_token'),
        },
      })
        .then(resp => { return resp.json() })
        .then(data => {
          if (data['error']) {
            showBanner('.banner.error', 'Произошла ошибка:'+data['error'])
            return false
          } else {
            return data['success']
          }
        })
      this.LoadFindAPRecs = false
    },
    changePeriods() {
      try {
        this.selectedPeriods = []
        let checkboxes = document.querySelectorAll("[name='periodsCheckbox']")
        for (let i=0;i<checkboxes.length;i++) {
          if (checkboxes[i].checked) {
            this.selectedPeriods.push(checkboxes[i].id)
          }
        }
      } catch (e) {}
      this.MaxRecsPage = false
      this.recs_page = 1
      this.counter = 0
      this.LoadRecs = true
      this.listRecs = []
      if (this.selectedPeriods.length !== this.listPeriods.length) {
        this.checkOneYearPeriod()
      } else {
        this.oneYearPeriod = false
      }
      this.getRecs()
      this.SideBoxChecked = false
    },
    async getRecs() {
      let url = this.$store.state.backendUrl+'/api/v1/admin/tables/wk14fp/'
      if (this.findString.length > 0) {
        url += '?'+this.findString
      }
      if (this.recs_page != 1) {
        if (this.findString.length > 0) {
          url += '&page='+this.recs_page
        } else {
          url += '?page='+this.recs_page
        }
      }
      let results = []
      await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': 'Token '+localStorage.getItem('access_token'),
        },
      })
        .then(resp => { return resp.json() })
        .then(data => {
          if (data['error']) {
            if (this.recs_page == 1) {
              showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
              return false
            } else {
              showBanner('.banner.success', 'Отображены все записи')
              this.MaxRecsPage = true
              return false
            }
          }
          results = data
        })
      this.counter = results.length
      for (let i=0;i<=results.length-1;i++) {
        if (this.selectedPeriods.length === this.listPeriods.length) {
          this.sourceRecs.push(results[i])
        } else {
          if (this.selectedPeriods.includes(results[i].year_start+'-'+results[i].year_end)) {
            this.sourceRecs.push(results[i])
          }
        }
      }
      let temp_list = []
      this.sourceRecs.map((kek) => {
        temp_list.push(kek)
      })
      this.listRecs = temp_list
      this.setFilterValues()
      this.LoadRecs = false
      this.recs_page += 1
      this.LoadClass = 'vue-deactive'
      this.ContentClass = 'vue-active'
    },
    setFilterValues() {
      this.listRecs.map((rec) => {
        rec.objects.map((obj) => {
          obj.purchases.map((purchase) => {
            this.fieldsList.map((field) => {
              if (!([null, undefined].includes(purchase[field.field]))) {
                if (!(this.tableFilters[field.field].allValues.includes(purchase[field.field]))) {
                  this.tableFilters[field.field].allValues.push(purchase[field.field])
                }
              }
            })
          })
        })
      })
      Object.keys(this.tableFilters).map((key) => {
        if (key.includes('date')) {
          this.tableFilters[key].allValues.sort((a,b) => new Date(a) - new Date(b))
        } else {
          this.tableFilters[key].allValues.sort((a,b) => a - b)
        }
      })
    },
    openFilter(selectedFilter) {
      this.selectedFilter = selectedFilter
      this.fieldsList.map((field) => {
        if (field.field === selectedFilter) {
          this.displayFilterName = field.alias
        }
      })
      this.openSideBox('filter')
    },
    addOrDeleteValueToFilter(value) {
      if (this.tableFilters[this.selectedFilter].selectedValues.includes(value)) {
        this.tableFilters[this.selectedFilter].selectedValues.splice(
          this.tableFilters[this.selectedFilter].selectedValues.indexOf(value), 1
        )
      } else {
        this.tableFilters[this.selectedFilter].selectedValues.push(value)
      }
    },
    filterRecs() {
      let count = 0
      Object.keys(this.tableFilters).map((field) => {
        if (this.tableFilters[field].selectedValues.length === 0) {
          count++
        }
      })
      if (count === this.fieldsList.length) {
        this.MaxRecsPage = false
        this.recs_page = 1
        this.counter = 0
        this.LoadRecs = true
        this.listRecs = []
        this.sourceRecs = []
        this.getRecs()
      } else {
        let recs = []
        this.listRecs.map((rec) => {
          recs.push(rec)
        })
        let filtering = []
        Object.keys(this.tableFilters).map((field) => {
          if (this.tableFilters[field].selectedValues.length > 0) {
            recs.map((rec) => {
              rec.objects.map((obj) => {
                obj.purchases.map((purchase) => {
                  if (this.tableFilters[field].selectedValues.includes(purchase[field])) {
                    if (filtering.filter((f_rec) => f_rec.object_uuid === rec.object_uuid).length === 0) {
                      let newFilterRec = rec
                      newFilterRec.objects = []
                      filtering.push(newFilterRec)
                    }
                    if (filtering.filter(
                      (f_rec) => f_rec.object_uuid === rec.object_uuid
                    )[0].objects.filter(
                      (f_obj) => f_obj.object_uuid === obj.object_uuid).length === 0
                    ) {
                      let newFilterObj = obj
                      newFilterObj.purchases = []
                      filtering.filter((f_rec) => f_rec.object_uuid === rec.object_uuid)[0].objects.push(newFilterObj)
                    }
                    if (!(filtering.filter(
                      (f_rec) => f_rec.object_uuid === rec.object_uuid
                    )[0].objects.filter(
                      (f_obj) => f_obj.object_uuid === obj.object_uuid)[0].purchases.includes(purchase))) {
                      filtering.filter(
                        (f_rec) => f_rec.object_uuid === rec.object_uuid
                      )[0].objects.filter(
                        (f_obj) => f_obj.object_uuid === obj.object_uuid)[0].purchases.push(purchase)
                    }
                  }
                })
              })
            })
          }
        })
        this.listRecs = filtering
      }
      this.SideBoxChecked = false
    },
    filterReset() {
      Object.keys(this.tableFilters).map((key) => {
        this.tableFilters[key].selectedValues = []
      })
      this.filterRecs()
    },
    openSideBox(action) {
      this.AddClass = 'sidebox-deactive'
      this.FindClass = 'sidebox-deactive'
      this.DetailClass = 'sidebox-deactive'
      this.FilterClass = 'sidebox-deactive'
      this.PeriodsClass = 'sidebox-deactive'
      switch (action) {
        case 'add':
          this.AddClass = 'sidebox-active'
          break

        case 'find':
          this.FindClass = 'sidebox-active'
          break

        case 'detail':
          this.DetailClass = 'sidebox-active'
          break

        case 'filter':
          this.FilterClass = 'sidebox-active'
          break

        default:
          this.PeriodsClass = 'sidebox-active'
      }
      this.SideBoxChecked = true
    },
    async getEvents() {
      this.listEvents = await fetch(this.$store.state.backendUrl+'/api/v1/guides/get_bank_events/', {
        method: 'GET',
        headers: {
          'Authorization': 'Token '+localStorage.getItem('access_token'),
        },
      })
        .then(resp => { return resp.json() })
        .then(data => {
          if (data['error']) {
            showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
            return false
          }
          return data
        })
    },
    async getMos() {
      this.listMos = await fetch(this.$store.state.backendUrl+'/api/v1/admin/oo/full_mos/', {
        method: 'GET',
        headers: {
          'Authorization': 'Token '+localStorage.getItem('access_token'),
        },
      })
        .then(resp => { return resp.json() })
        .then(data => {
          if (data['error']) {
            showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
            return false
          }
          return data
        })
    },
    async deleteWK14FP(uuid) {
      if (confirm('Вы уверены, что хотите удалить запись?')) {
        this.LoadRecs = true
        this.listRecs = []
        this.recs_page = 1
        this.MaxRecsPage = false
        let url = this.$store.state.backendUrl+'/api/v1/admin/tables/wk14fp/'+uuid+'/'
        await fetch(url, {
          method: 'delete',
          headers: {
            'X-CSRFToken': getCookie("csrftoken"),
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': 'Token '+localStorage.getItem('access_token')
          }
        })
          .then(resp => { return resp.json()})
          .then(data => {
            if (data.success) {
              showBanner('.banner.success', data['success'])
              this.getRecs()
            } else {
              showBanner('.banner.error', data['error'])
              return false
            }
          })

      }
    },
    async deletePurchase(uuid) {
      if (confirm('Вы уверены, что хотите удалить закупку/контракт?')){
        this.LoadRecs = true
        this.listRecs = []
        this.recs_page = 1
        this.MaxRecsPage = false
        let url = this.$store.state.backendUrl+'/api/v1/admin/tables/purchasewk14fp/'+uuid+'/'
        await fetch(url, {
          method: 'delete',
          headers: {
            'X-CSRFToken': getCookie("csrftoken"),
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': 'Token '+localStorage.getItem('access_token')
          }
        })
          .then(resp => { return resp.json()})
          .then(data => {
            if (data.success) {
              showBanner('.banner.success', data['success'])
            } else {
              showBanner('.banner.error', data['error'])
              return false
            }
          })
      }
      this.getRecs()
    },
    async addOfficial(uuid) {
      this.LoadOFRecs = true
      this.LoadRecs = true
      this.listRecs = []
      this.recs_page = 1
      this.MaxRecsPage = false
      let url = this.$store.state.backendUrl+'/api/v1/admin/tables/ofwk14fp/'
      await fetch(url, {
        method: 'post',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'application/json;charset=UTF-8',
          'Authorization': 'Token '+localStorage.getItem('access_token')
        },
        body: JSON.stringify({
          'wk14fp_uuid': this.editAPUuid,
          'official_uuid': uuid
        })
      })
        .then(resp => { return resp.json()})
        .then(data => {
          if (data.success) {
            showBanner('.banner.success', data['success'])
          } else {
            showBanner('.banner.error', data['error'])
            return false
          }
        })
      this.getOfRecs()
      this.getRecs()
    },
    async deleteOfficial(uuid) {
      if (confirm('Вы уверены, что хотите удалить должностное лицо?')){
        this.LoadOFRecs = true
        this.LoadRecs = true
        this.listRecs = []
        this.recs_page = 1
        this.MaxRecsPage = false
        let url = this.$store.state.backendUrl+'/api/v1/admin/tables/ofwk14fp/'+this.editAPUuid+'/?official_uuid='+uuid
        let data = new FormData()
        data.append('official_uuid', uuid)
        await fetch(url, {
          method: 'delete',
          headers: {
            'X-CSRFToken': getCookie("csrftoken"),
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': 'Token '+localStorage.getItem('access_token')
          }
        })
          .then(resp => { return resp.json()})
          .then(data => {
            if (data.success) {
              showBanner('.banner.success', data['success'])
            } else {
              showBanner('.banner.error', data['error'])
              return false
            }
          })
      }
      this.getOfRecs()
      this.getRecs()
    },
    async addCP(uuid) {
      this.LoadCPRecs = true
      this.LoadRecs = true
      this.listRecs = []
      this.recs_page = 1
      this.MaxRecsPage = false
      let url = this.$store.state.backendUrl+'/api/v1/admin/tables/cpwk14fp/'
      await fetch(url, {
        method: 'post',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'application/json;charset=UTF-8',
          'Authorization': 'Token '+localStorage.getItem('access_token')
        },
        body: JSON.stringify({
          'wk14fp_uuid': this.editAPUuid,
          'cp_uuid': uuid
        })
      })
        .then(resp => { return resp.json()})
        .then(data => {
          if (data.success) {
            showBanner('.banner.success', data['success'])
          } else {
            showBanner('.banner.error', data['error'])
            return false
          }
        })
      this.getCPRecs()
      this.getRecs()
    },
    async deleteCP(uuid) {
      if (confirm('Вы уверены, что хотите удалить контактное лицо?')){
        this.LoadCPRecs = true
        this.LoadRecs = true
        this.listRecs = []
        this.recs_page = 1
        this.MaxRecsPage = false
        let url = this.$store.state.backendUrl+'/api/v1/admin/tables/cpwk14fp/'+this.editAPUuid+'/?cp_uuid='+uuid
        let data = new FormData()
        data.append('official_uuid', uuid)
        await fetch(url, {
          method: 'delete',
          headers: {
            'X-CSRFToken': getCookie("csrftoken"),
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': 'Token '+localStorage.getItem('access_token')
          }
        })
          .then(resp => { return resp.json()})
          .then(data => {
            if (data.success) {
              showBanner('.banner.success', data['success'])
            } else {
              showBanner('.banner.error', data['error'])
              return false
            }
          })
      }
      this.getCPRecs()
      this.getRecs()
    },
    async add14FPRec() {
      if (this.addMo === '') {
        showBanner('.banner.error', 'Заполните поле "МО"')
        return false
      }
      if (this.addYearStart === '') {
        showBanner('.banner.error', 'Заполните поле "Год начала реализации"')
        return false
      }
      if (this.addYearEnd === '') {
        showBanner('.banner.error', 'Заполните поле "Год окончания реализации"')
        return false
      }
      this.LoadOFRecs = true
      this.LoadRecs = true
      this.listRecs = []
      this.recs_page = 1
      this.MaxRecsPage = false
      let url = this.$store.state.backendUrl+'/api/v1/admin/tables/wk14fp/'
      await fetch(url, {
        method: 'post',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'application/json;charset=UTF-8',
          'Authorization': 'Token '+localStorage.getItem('access_token')
        },
        body: JSON.stringify({
          'mo': this.listMos.filter((mo) => mo.name === this.addMo)[0].object_uuid,
          'year_start': this.addYearStart,
          'year_end': this.addYearEnd
        })
      })
        .then(resp => { return resp.json()})
        .then(data => {
          if (data.success) {
            showBanner('.banner.success', data['success'])
            this.SideBoxChecked = false
          } else {
            showBanner('.banner.error', data['error'])
            return false
          }
        })
      this.getRecs()
    },
    findRecs() {
      this.findString = ''
      this.MaxRecsPage = false
      this.recs_page = 1
      this.counter = 0
      this.LoadRecs = true
      this.listRecs = []
      if ((this.findMo != '') &&
        (this.findMo != null)) {
        this.findString += 'mo='+this.findMo
      }
      if ((this.findYearStart != '') &&
        (this.findYearStart != null)) {
        this.findString += '&year_start='+this.findYearStart
      }
      if ((this.findYearEnd != '') &&
        (this.findYearEnd != null)) {
        this.findString += '&year_end='+this.findYearEnd
      }
      if ((this.findOoShortName != '') &&
        (this.findOoShortName != null)) {
        this.findString += '&oo='+this.findOoShortName
      }
      if ((this.findOoAddress != '') &&
        (this.findOoAddress != null)) {
        this.findString += '&address='+this.findOoAddress
      }
      this.getRecs()
      this.SideBoxChecked = false
    },
    findAPRecs() {
      this.findAPString = ''
      this.LoadFindAPRecs = true
      this.listFindAPRecs = []
      if ((this.findApSurname != '') &&
        (this.findApSurname != null)) {
        this.findAPString += 'surname='+this.findApSurname
      }
      if ((this.findApName != '') &&
        (this.findApName != null)) {
        this.findAPString += '&name='+this.findApName
      }
      if ((this.findApPatronymic != '') &&
        (this.findApPatronymic != null)) {
        this.findAPString += '&patronymic='+this.findApPatronymic
      }
      if ((this.findApPost != '') &&
        (this.findApPost != null)) {
        this.findAPString += '&post='+this.findApPost
      }
      if ((this.findApPhone != '') &&
        (this.findApPhone != null)) {
        this.findAPString += '&phone='+this.findApPhone
      }
      this.getFindAPRecs()
    },
    checkAPInOfficials(uuid) {
      let check = false
      for(let i=0;i<this.listOFRecs.length;i++){
        if (this.listOFRecs[i].object_uuid == uuid) {
          check = true
          break;
        }
      }
      return check
    },
    checkAPInCp(uuid) {
      let check = false
      for(let i=0;i<this.listCPRecs.length;i++){
        if (this.listCPRecs[i].object_uuid == uuid) {
          check = true
          break;
        }
      }
      return check
    },
    checkContractPrice(type) {
      let price = 0.0
      if (type == 'new') {
        price = this.newRecContractPrice
      } else {
        price = this.editRecContractPrice
      }
      if ((price != 0.0) && (price != null)) {
        if (this.SubsidyInfo.balance) {
          if (type == 'new') {
            if (this.convertMoneyToNumber(price) >=
              Number(this.SubsidyInfo.balance)) {
              this.ContractPriceTooMuch = true
              return true
            } else {
              this.ContractPriceTooMuch = false
              return true
            }
          } else {
            if (this.convertMoneyToNumber(price) >=
              Number(this.editBalance)) {
              this.ContractPriceTooMuch = true
              return true
            } else {
              this.ContractPriceTooMuch = false
              return true
            }
          }
        }
      }
    },
    getYearStartFromPeriod(period) {
      let arr = period.split('-')
      return arr[0]
    },
    getYearEndFromPeriod(period) {
      let arr = period.split('-')
      return arr[1]
    },
    format(inputDate) {
      let day, month, year;

      day = inputDate.substring(8,10)
      month = inputDate.substring(5, 7)
      year = inputDate.substring(0, 4)

      return `${day}.${month}.${year}`;
    },
    convertStrDate(str){
      return convertStrToDate(str)
    },
    checkUrl(str) {
      return isValidHttpUrl(str)
    },
    async downloadExcel() {
      this.downloadLoad = true
      let url = this.$store.state.backendUrl+'/api/v1/admin/excel/wk14fp/'
      if (this.findString.length > 0) {
        url += '?'+this.findString
      }
      if (this.selectPeriod == 'Все') {
        if (this.findString.length > 0) {
          url += '&is_period=false'
        } else {
          url += '?is_period=false'
        }
      } else {
        if (this.findString.length > 0) {
          url += '&is_period=true&period='+this.selectPeriod
        } else {
          url += '?is_period=true&period='+this.selectPeriod
        }
      }
      await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': 'Token '+localStorage.getItem('access_token'),
        },
      })
        .then(res => {
          this.downloadLoad = false
          return res.blob()
        })
        .then(data => {
          var file = window.URL.createObjectURL(data);
          window.location.assign(file);
        })
    },
  },
  created() {
    this.getRecs()
    this.getEvents()
    this.getPeriods()
    this.getMos()
  },
  updated(){
    ResizeTables()
  }
}
</script>

<style>
.mini-font {
  font-size: 12px;
}
.makro-font {
  font-size: 10px;
}
.text-area-size {
  height: 75px;
}
.edit_purchase_hide {
  visibility: collapse;
}
.edit_purchase_show {
  visibility: visible;
}
</style>
