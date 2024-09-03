<template>

    <v-icon
        v-if="bool"
        icon="mdi-check"
        color="green"
    />

    <v-icon
        v-if="!bool"
        icon="mdi-cancel"
        color="red"
    />

</template>

<script>

export default {
  name: 'BooleanBadge',
  props: {
    bool: Boolean, // Получение значение (true или false)
  }
}

</script>

<style scoped>

</style>