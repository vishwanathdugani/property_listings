<template>
  <div class="home-container">
    <div class="content">
      <div class="filters">
        <input type="text" placeholder="Address" v-model="filters.address" />
        <input type="text" placeholder="Class" v-model="filters.class" />
        <div class="slider-container">
          <label for="estimatedMarketValue">Estimated Market Value:</label>
          <input type="range" id="estimatedMarketValue" v-model="filters.estimatedMarketValueMin" min="0" max="1000000" step="1000">
          <span>{{ filters.estimatedMarketValueMin }}</span> to
          <input type="range" id="estimatedMarketValueMax" v-model="filters.estimatedMarketValueMax" min="0" max="1000000" step="1000">
          <span>{{ filters.estimatedMarketValueMax }}</span>
        </div>
        <div class="slider-container">
          <label for="buildingSqFt">Building Sq Ft:</label>
          <input type="range" id="buildingSqFt" v-model="filters.buildingSqFtMin" min="0" max="10000" step="10">
          <span>{{ filters.buildingSqFtMin }}</span> to
          <input type="range" id="buildingSqFtMax" v-model="filters.buildingSqFtMax" min="0" max="10000" step="10">
          <span>{{ filters.buildingSqFtMax }}</span>
        </div>
        <input type="text" placeholder="BLDG_USE" v-model="filters.bldgUse" />
        <div class="filter-buttons">
          <button @click="fetchProperties">Apply Filters</button>
          <button @click="clearFilters">Clear Filters</button>
        </div>
        <div v-if="!isValidRange" class="error-message">
          Minimum values must be less than or equal to maximum values.
        </div>
      </div>
      <div class="properties-list">
        <h3>Properties</h3>
        <div class="pagination-buttons">
          <button @click="firstPage">First Page</button>
          <button @click="previousPage">Previous Page</button>
          <button @click="nextPage" v-if="moreExists">Next Page</button>
        </div>
        <ul>
          <li v-for="property in properties" :key="property.id">
            <router-link :to="{ name: 'PropertyDetails', params: { id: property.id }}" class="property-link">
              <div>{{ property.full_address }}</div>
              <div>Class: {{ property.class_description }}</div>
              <div>BLDG_USE: {{ property.bldg_use }}</div>
              <div>Estimated Market Value: ${{ property.estimated_market_value.toLocaleString() }}</div>
              <div>Building Sq Ft: {{ property.building_sq_ft }}</div>
            </router-link>
          </li>
        </ul>
      </div>
      <div class="map-view" v-if="properties.length">
        <l-map :zoom="zoomLevel" :center="mapCenter" style="height: 100%">
          <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"></l-tile-layer>
          <l-marker v-for="property in properties" :key="property.id" :lat-lng="[property.latitude, property.longitude]" @click="navigateToProperty(property.id)">
          </l-marker>
        </l-map>
      </div>
    </div>
  </div>
</template>




<script>
import { ref, computed } from 'vue';
import { LMap, LTileLayer, LMarker } from 'vue3-leaflet';
import 'leaflet/dist/leaflet.css';
import { useRouter } from 'vue-router';
import http from '@/http';

export default {
  name: 'HomeView',
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },


  setup() {
    const router = useRouter();
    const properties = ref([]);
    const currentPage = ref(0);
    const moreExists = ref(false);
    const limit = ref(25); // Adjust as needed
    const filters = ref({
      address: '',
      class: '',
      bldgUse: '',
      estimatedMarketValueMin: 0,
      estimatedMarketValueMax: 10000000,
      buildingSqFtMin: 0,
      buildingSqFtMax: 10000,
    });

    const mapCenter = computed(() => {
    if (!properties.value.length) return [0, 0];
    const { totalLat, totalLng } = properties.value.reduce((acc, cur) => {
      return {
        totalLat: acc.totalLat + cur.latitude,
        totalLng: acc.totalLng + cur.longitude,
      };
    }, { totalLat: 0, totalLng: 0 });

    const avgLat = totalLat / properties.value.length;
    const avgLng = totalLng / properties.value.length;

  return [avgLat, avgLng];
});

  const zoomLevel = ref(12); 

  const fetchProperties = async () => {

    if (!isValidRange.value) {
    console.error("Invalid range: Min values must be <= Max values.");
  }

  try {
    const skip = currentPage.value * limit.value;
    const response = await http.get('properties_listings/', {
      params: {
        full_address: filters.value.address,
        class_description: filters.value.class,
        bldg_use: filters.value.bldgUse,
        estimated_market_value_min: filters.value.estimatedMarketValueMin,
        estimated_market_value_max: filters.value.estimatedMarketValueMax,
        building_sq_ft_min: filters.value.buildingSqFtMin,
        building_sq_ft_max: filters.value.buildingSqFtMax,
        skip: skip,
        limit: limit.value,
      },
    });

    properties.value = response.data.properties;
    moreExists.value = response.data.moreExists;

  } 
  catch (error) {
    console.error("Failed to fetch properties:", error);
  }

  };

  const navigateToProperty = (propertyId) => {
  router.push(`/properties/${propertyId}`);
  };

      const nextPage = () => {
      if (moreExists.value) {
        currentPage.value++;
        fetchProperties();
      }
    };

    const isValidRange = computed(() => {
      return filters.value.estimatedMarketValueMin <= filters.value.estimatedMarketValueMax && 
            filters.value.buildingSqFtMin <= filters.value.buildingSqFtMax;
    });

    const firstPage = () => {
      currentPage.value = 0;
      fetchProperties();
    };

    const previousPage = () => {
      if (currentPage.value > 0) {
        currentPage.value--;
        fetchProperties();
        console.log('Current page after decrement:', currentPage.value); // Debugging
      }
    };

    const clearFilters = () => {
      filters.value = {
        address: '',
        class: '',
        bldgUse: '',
        estimatedMarketValueMin: 0,
        estimatedMarketValueMax: 10000000,
        buildingSqFtMin: 0,
        buildingSqFtMax: 10000,
      };
    };

  fetchProperties();

  return {
      properties,
      filters,
      fetchProperties,
      nextPage,
      moreExists,
      mapCenter,
      zoomLevel,
      navigateToProperty,
      clearFilters,
      firstPage,
      previousPage,
      isValidRange,
      };
    },
  };
  </script>



<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  max-width: 1200px;
  margin: 20px auto;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.content {
  display: flex;
  gap: 20px;
}

.filters {
  flex: 1;
  margin-right: 20px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.properties-list {
  flex: 2;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 20px;
  overflow: hidden;
}

.map-view {
  flex: 2;
  background-color: #ececec;
  border-radius: 8px;
  overflow: hidden;
  height: 600px;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  padding: 15px;
  border-bottom: 1px solid #ddd;
  transition: background-color 0.3s ease;
}

li:last-child {
  border-bottom: none;
}

li:hover {
  background-color: #f6f6f6;
}

.property-link {
  color: #333;
  text-decoration: none;
  display: block; 
}

.filter-buttons, .pagination-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

button:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
}

.slider-container {
  margin-bottom: 15px;
}

label {
  font-weight: bold;
  color: #555;
  margin-bottom: 5px;
}

input[type="text"], input[type="range"], select {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 8px;
  width: 100%;
}

.error-message {
  color: red;
  margin-top: 10px;
}

h3 {
  font-family: 'Roboto', sans-serif; 
  font-weight: 700; 
  color: #333;
  margin-bottom: 20px; 
}
</style>
