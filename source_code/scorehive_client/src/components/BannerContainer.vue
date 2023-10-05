<template>
    <div :class="containerClass" class="containerClass"
        :style="{ width: containerWidth, height: containerHeight, borderRadius: borderRadius }">
        <img v-if="showImage" :src="bannerUrl" class="img-thumbnail" alt="Selected image"
            :style="{ width: containerWidth, height: containerHeight, borderRadius: borderRadius }" />
        <div v-else class="empty-image"
            :style="{ width: containerWidth, height: containerHeight, borderRadius: borderRadius }">
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
        bannerUrl: {
            type: String,
            default: '',
        },
        emptyImageContent: {
            type: String,
            default: 'BANNER',
        },
        containerWidth: {
            type: String,
            default: '150px',
        },
        containerHeight: {
            type: String,
            default: '150px',
        },
        borderRadius: {
            type: String,
            default: '50%',
        },
    },
    computed: {
        containerClass() {
            return this.showImage ? 'image-container' : 'empty-image';
        },

    },
};
</script>

<style scoped>
.containerClass {
    position: relative;
    display: flexbox;
    justify-content: center;
    align-items: center;
    background-color: #f2f2f2;
    width: 1000px;
}

.img-thumbnail {
    object-fit: cover;
    width: 1000px;
}

.empty-image {
  width:5000px;
  height: 150px;
  background-color: #f2f2f2;
  border-radius: 10%;
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