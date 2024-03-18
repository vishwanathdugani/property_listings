<template>
  <div class="home-container">
    <div class="content">
      <div class="filters">
        <input type="text" placeholder="Address" v-model="filters.address" />
        <input type="text" placeholder="Class" v-model="filters.class" />
        <div>
          <label for="estimatedMarketValue">Estimated Market Value:</label>
          <input type="range" id="estimatedMarketValue" v-model="filters.estimatedMarketValueMin" min="0" max="1000000" step="1000">
          <span>{{filters.estimatedMarketValueMin}}</span>
          to
          <input type="range" id="estimatedMarketValueMax" v-model="filters.estimatedMarketValueMax" min="0" max="1000000" step="1000">
          <span>{{filters.estimatedMarketValueMax}}</span>
        </div>
        <div>
          <label for="buildingSqFt">Building Sq Ft:</label>
          <input type="range" id="buildingSqFt" v-model="filters.buildingSqFtMin" min="0" max="10000" step="10">
          <span>{{filters.buildingSqFtMin}}</span>
          to
          <input type="range" id="buildingSqFtMax" v-model="filters.buildingSqFtMax" min="0" max="10000" step="10">
          <span>{{filters.buildingSqFtMax}}</span>
        </div>

        <input type="text" placeholder="BLDG_USE" v-model="filters.bldgUse" />
        <!-- Add buttons or methods to apply/clear filters -->
        <button @click="fetchProperties">Apply Filters</button>
      </div>
      <div class="properties-list">
      <h3>Properties</h3>
      <ul>
        <li v-for="property in properties" :key="property.id">
          <router-link v-if="property.id" :to="{ name: 'PropertyDetails', params: { id: property.id }}">
            {{ property.full_address }}, Class: {{ property.class_description }}, BLDG_USE: {{ property.bldg_use }},
            Estimated Market Value: {{ property.estimated_market_value }}, Building Sq Ft: {{ property.building_sq_ft }}
          </router-link>
        </li>
      </ul>
    </div>
    </div>
  </div>
</template>

<script>
import http from '@/http';
import { ref } from 'vue';

export default {
  name: 'HomeView',
  setup() {
    const properties = ref([]);
    const filters = ref({
      address: '',
      class: '',
      bldgUse: '',
      estimatedMarketValueMin: 0,
      estimatedMarketValueMax: 1000000,
      buildingSqFtMin: 0,
      buildingSqFtMax: 10000,
    });

    const fetchProperties = async () => {
      try {
        const response = await http.get('properties_listings/', {
          params: {
            full_address: filters.value.address,
            class_description: filters.value.class,
            bldg_use: filters.value.bldgUse,
            estimated_market_value_min: filters.value.estimatedMarketValueMin,
            estimated_market_value_max: filters.value.estimatedMarketValueMax,
            building_sq_ft_min: filters.value.buildingSqFtMin,
            building_sq_ft_max: filters.value.buildingSqFtMax,
          },
        });
        console.log(response.data);
        properties.value = response.data;
      } catch (error) {
        console.error("Failed to fetch properties:", error);
      }
    };

    fetchProperties();

    return {
      properties,
      filters,
      fetchProperties,
    };
  },
};
</script>




<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.content {
  display: flex;
  gap: 20px; /* Creates space between the filters and the property list */
}

.filters {
  flex-basis: 20%;
  display: flex;
  flex-direction: column;
  gap: 10px; /* Creates space between filter inputs */
}

.properties-list {
  flex-grow: 1;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
}

/* Styling for the router link to make it look more like a card */
.router-link-active {
  display: block;
  background-color: #f9f9f9;
  padding: 10px;
  border-radius: 5px;
  color: #333;
  text-decoration: none;
  border: 1px solid #ddd;
  transition: all 0.3s ease;
}

.router-link-active:hover {
  background-color: #eee;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

/* Styling for search bars and sliders */
input[type="text"], input[type="range"] {
  width: 100%;
  padding: 8px;
  margin: 4px 0;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* Styling for buttons */
button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}

/* Labels for sliders */
label {
  font-size: 14px;
  color: #666;
}

/* Styling for the range input (slider) */
input[type="range"] {
  -webkit-appearance: none; /* Override default CSS styles */
  appearance: none;
  width: 100%;
  height: 8px;
  background: #ddd;
  outline: none;
  opacity: 0.7;
  -webkit-transition: .2s;
  transition: opacity .2s;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  background: #007bff;
  cursor: pointer;
  border-radius: 50%;
}

input[type="range"]::-moz-range-thumb {
  width: 20px;
  height: 20px;
  background: #007bff;
  cursor: pointer;
  border-radius: 50%;
}
</style>

