<template>
  <LkPage :usePreLoader="usePreLoader">
    <slot>
      <v-card
          variant="outlined"
      >
        <v-card-text>
          <div style="background-color: white; overflow: auto;" class="adaptive-no-tab-table-card-text">
            <v-tabs
              v-model="guidesTab"
              bg-color="coko-blue"
              show-arrows
            >

              <v-tab class="coko-tab" value="state">Государства</v-tab>
              <v-tab class="coko-tab" value="mo">МО</v-tab>
              <v-tab class="coko-tab" value="oo_type">Типы ОО</v-tab>
              <v-tab class="coko-tab" value="oo">ОО</v-tab>
              <v-tab class="coko-tab" value="audience_category">Категории слушателей</v-tab>
              <v-tab class="coko-tab" value="event_type">Типы мероприятий</v-tab>
              <v-tab class="coko-tab" value="position_category">Категории должностей</v-tab>
              <v-tab class="coko-tab" value="position">Должности</v-tab>

            </v-tabs>

            <GuideState v-if="guidesTab === 'state'" />

            <GuideMo v-if="guidesTab === 'mo'" />

            <GuideOoType v-if="guidesTab === 'oo_type'" />

            <GuideOo v-if="guidesTab === 'oo'" />

            <GuideAudienceCategory v-if="guidesTab === 'audience_category'" />

            <GuideEventType v-if="guidesTab === 'event_type'" />

            <GuidePositionCategory v-if="guidesTab === 'position_category'" />

            <GuidePosition v-if="guidesTab === 'position'" />

          </div>
        </v-card-text>
      </v-card>
    </slot>
  </LkPage>
</template>

<script>
import LkPage from "@/components/LkPage.vue";
import GuideState from "@/views/administrator/guides/GuideState.vue";
import GuideMo from "@/views/administrator/guides/GuideMo.vue";
import GuideOoType from "@/views/administrator/guides/GuideOoType.vue";
import GuideOo from "@/views/administrator/guides/GuideOo.vue";
import GuideAudienceCategory from "@/views/administrator/guides/GuideAudienceCategory.vue";
import GuideEventType from "@/views/administrator/guides/GuideEventType.vue";
import GuidePositionCategory from "@/views/administrator/guides/GuidePositionCategory.vue";
import GuidePosition from "@/views/administrator/guides/GuidePosition.vue";

export default {
  name: "Guides",
  components: {
    GuidePosition,
    GuidePositionCategory,
    GuideEventType, GuideAudienceCategory, GuideOo, GuideOoType, GuideMo, GuideState, LkPage},
  props: {
    usePreLoader: Function,
  },
  data() {
    return {
      guidesTab: 'state'
    }
  },
  mounted() {
    this.usePreLoader(true)
  }
}
</script>

<style scoped>

</style>
