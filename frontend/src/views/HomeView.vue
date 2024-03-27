<template>
  <div class="home-container">
    <div class="content">
      <div class="filters">
        <input type="text" placeholder="Address" v-model="filters.address" />
        <input type="text" placeholder="Class" v-model="filters.class" />
        <div class="slider-container">
          <label for="estimatedMarketValueRange" class="slider-label">Estimated Market Value Range:</label>
          <div class="slider-container">
          <VueSlider v-model="filters.estimatedMarketValueRange" :min="sliderRanges.estimatedMarketValue.min" :max="sliderRanges.estimatedMarketValue.max" :enable-cross="false" :tooltip="'always'"/>
          </div>
        </div>
        <div class="slider-container">
          <label for="buildingSqFtRange" class="slider-label">Building Sq Ft Range:</label>
          <div class="slider-container">
          <VueSlider v-model="filters.buildingSqFtRange" :min="sliderRanges.buildingSqFt.min" :max="sliderRanges.buildingSqFt.max" :enable-cross="false" :tooltip="'always'"/>
        </div>
        </div>
        <input type="text" placeholder="BLDG_USE" v-model="filters.bldgUse" />
        <div class="filter-buttons">
          <button @click="fetchProperties">Apply Filters</button>
          <button @click="clearFilters">Clear Filters</button>
        </div>
        
      </div>
      <div class="properties-list">
        <h2>Properties</h2>
        <div class="pagination-buttons">
          <a href="#" @click.prevent="firstPage" v-if="currentPage > 0">First Page</a> 
          <a href="#" @click.prevent="previousPage" v-if="currentPage > 0">Previous Page</a> 
          <a href="#" @click.prevent="nextPage" v-if="moreExists">Next Page</a>
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
        <div class="pagination-buttons">
  <a href="#" @click.prevent="firstPage" v-if="currentPage > 0">First Page</a> 
  <a href="#" @click.prevent="previousPage" v-if="currentPage > 0">Previous Page</a> 
  <a href="#" @click.prevent="nextPage" v-if="moreExists">Next Page</a>
</div>
      </div>
      <div class="map-view" v-if="properties && properties.length > 0">

        <l-map
          ref="mapInstance"
          :zoom="zoomLevel"
          :center="mapCenter"
          style="height: 100%"
          @update:zoom="zoomLevel = $event"
          @update:center="mapCenter = $event"
          >
          <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" ></l-tile-layer>
          <l-marker v-for="property in properties" :key="property.id" :lat-lng="[property.latitude, property.longitude]" @click="navigateToProperty(property.id)">
            <!-- <l-tooltip>
              {{ property.full_address || 'Loading address...' }}
      </l-tooltip> -->
          </l-marker>
        </l-map>
      </div>
    </div>
  </div>
</template>


<script>
import { ref, computed, onMounted, watch } from 'vue';
// import { LMap, LTileLayer, LMarker, LTooltip } from 'vue3-leaflet';
import { LMap, LTileLayer, LMarker } from 'vue3-leaflet';
import 'leaflet/dist/leaflet.css';
import { useRouter } from 'vue-router';
import http from '@/http';
import VueSlider from 'vue-slider-component';
import 'vue-slider-component/theme/default.css'


export default {
  name: 'HomeView',
  components: {
    LMap,
    LTileLayer,
    LMarker,
    VueSlider,
    // LTooltip
  },

  
  setup() {
    const router = useRouter();
    const properties = ref([]);
    const currentPage = ref(0);
    const moreExists = ref(false);
    const limit = ref(25); // Adjust as needed
    const mapInstance = ref(null);
    
    watch(properties, (newProperties) => {
      if (newProperties.length > 0 && mapInstance.value) {
        const bounds = newProperties.map(property => [property.latitude, property.longitude]);
        mapInstance.value.fitBounds(bounds);
      }
    }, { deep: true, immediate: true });

    const filters = ref({
      address: '',
      class: '',
      bldgUse: '',
      estimatedMarketValueRange: [0, 20000000],
      buildingSqFtRange: [0, 20000],
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
  try {
    const skip = currentPage.value * limit.value;
    const response = await http.get('properties_listings/', {
      params: {
        full_address: filters.value.address,
        class_description: filters.value.class,
        bldg_use: filters.value.bldgUse,
        estimated_market_value_min: filters.value.estimatedMarketValueRange[0],
        estimated_market_value_max: filters.value.estimatedMarketValueRange[1],
        building_sq_ft_min: filters.value.buildingSqFtRange[0],
        building_sq_ft_max: filters.value.buildingSqFtRange[1],
        skip: skip,
        limit: limit.value,
      },
    });
    console.log(response.data);
    properties.value = response.data.data; // Adjust this line based on actual response structure
    moreExists.value = response.data.more_exists; // Ensure this matches the backend's response
  } catch (error) {
    console.error("Failed to fetch properties:", error);
  }
};


onMounted(() => {
  fetchSliderRanges().then(fetchProperties);
});


  const sliderRanges = ref({
      estimatedMarketValue: { min: 0, max: 1000000 },
      buildingSqFt: { min: 0, max: 10000 },
    });


    const fetchSliderRanges = async () => {
  try {
    const { data } = await http.get('/properties/range');
    // Update the slider ranges in filters
    filters.value.estimatedMarketValueRange = [
      data.estimated_market_value.min, 
      data.estimated_market_value.max,
    ];
    filters.value.buildingSqFtRange = [
      data.building_sq_ft.min, 
      data.building_sq_ft.max,
    ];
    // Update sliderRanges for component knowledge
    sliderRanges.value = {
      estimatedMarketValue: {
        min: data.estimated_market_value.min,
        max: data.estimated_market_value.max,
      },
      buildingSqFt: {
        min: data.building_sq_ft.min,
        max: data.building_sq_ft.max,
      },
    };
  } catch (error) {
    console.error("Failed to fetch slider ranges:", error);
  }
};

onMounted(fetchSliderRanges);


  const navigateToProperty = (propertyId) => {
  router.push(`/properties/${propertyId}`);
  };

      const nextPage = () => {
      if (moreExists.value) {
        currentPage.value++;
        fetchProperties();
      }
    };

    const firstPage = () => {
      currentPage.value = 0;
      fetchProperties();
    };

    const previousPage = () => {
      if (currentPage.value > 0) {
        currentPage.value--;
        fetchProperties();
        console.log('Current page after decrement:', currentPage.value);
      }
    };

    const clearFilters = () => {
  filters.value = {
    address: '',
    class: '',
    bldgUse: '',
    estimatedMarketValueRange: [
      sliderRanges.value.estimatedMarketValue.min, 
      sliderRanges.value.estimatedMarketValue.max
    ],
    buildingSqFtRange: [
      sliderRanges.value.buildingSqFt.min, 
      sliderRanges.value.buildingSqFt.max
    ],
  };
};


  fetchProperties;

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
      sliderRanges,
      mapInstance,
      currentPage
      };
    },
  };
  </script>


<style scoped>
.content {
  display: flex;
  gap: 20px;
  justify-content: space-between;
  margin: 0 40px;
}

.filters, .properties-list, .map-view {
  flex: 1;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 20px;
}

.filters {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.properties-list {
  background-color: #fff;
  padding: 20px;
}

.map-view {
  background-color: #eeeeee;
  border: 1px solid #ddd;
  height: 600px;
}

ul, li {
  margin-top: 20px;
  list-style: none;
  padding: 10px;
  margin: 0;
}

li {
  margin-bottom: 10px;
  transition: background-color 0.3s ease;
}

li:hover {
  background-color: #f6f6f6;
}

.property-link {
  color: #333;
  text-decoration: none;
}

.property-link > div {
  margin-bottom: 5px;
}

.property-link > div:first-child {
  font-weight: bold;
  color: #007bff;
}

.filter-buttons button, .pagination-buttons a {
  background-color: #007bff;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-decoration: none;
}

.pagination-buttons a {
  background-color: transparent;
  color: #007bff;
  margin: 0 10px;
}

.filter-buttons button:hover, .pagination-buttons a:hover {
  background-color: #0056b3;
}

.sorting-container select {
  padding: 10px;
  margin-top: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

</style>


