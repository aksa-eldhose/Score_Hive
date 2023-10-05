<template>
  <div
    :class="containerClass"
    class="containerClass"
    :style="{
      width: containerWidth,
      height: containerHeight,
      borderRadius: borderRadius,
    }"
  >
    <img
      v-if="showImage"
      :src="imageUrl"
      class="img-thumbnail"
      alt="Selected image"
      :style="{
        width: containerWidth,
        height: containerHeight,
        borderRadius: borderRadius,
      }"
    />
    <div
      v-else
      class="empty-image"
      :style="{
        width: containerWidth,
        height: containerHeight,
        borderRadius: borderRadius,
      }"
    >
      <span class="empty-image-content">{{ emptyImageContent }}</span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    showImage: {
      type: Boolean,
      required: true,
    },
    imageUrl: {
      type: String,
      default: "",
    },
    emptyImageContent: {
      type: String,
      default: "LOGO",
    },
    containerWidth: {
      type: String,
      default: "150px",
    },
    containerHeight: {
      type: String,
      default: "150px",
    },
    borderRadius: {
      type: String,
      default: "50%",
    },
  },
  computed: {
    containerClass() {
      return this.showImage ? "" : "empty-image";
    },
  },
};
</script>

<style scoped>

.empty-image {
  background-color: #f2f2f2;
}

.empty-image-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-family: Poppins, sans-serif;
  font-size: 16px;
  font-weight: bold;
  color: #b3b3b3;
  letter-spacing: 2px;
}
</style>
