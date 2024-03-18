<template>
  <div class="home">
    <div class="filters">
      <!-- Filters will go here -->
    </div>
    <div class="properties">
      <div v-for="property in properties" :key="property.id" class="property">
        <h2>{{ property.full_address }}</h2>
        <p>Class: {{ property.class_description }}</p>
        <p>Estimated Market Value: ${{ property.estimated_market_value }}</p>
        <p>Building Use: {{ property.bldg_use }}</p>
        <p>Building Sq Ft: {{ property.building_sq_ft }}</p>
        <!-- More property details can be added here -->
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HomeView',
  data() {
    return {
      properties: [],
    };
  },
  async created() {
    try {
      const response = await axios.get('http://localhost:8000/properties_listings/');
      this.properties = response.data;
    } catch (error) {
      console.error("Failed to fetch properties:", error);
    }
  },
}
</script>

<style scoped>
.properties {
  display: flex;
  flex-wrap: wrap;
}

.property {
  flex-basis: calc(33.333% - 20px);
  margin: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}
</style>

/* .filters {
  /* Style your filters container */
} */


