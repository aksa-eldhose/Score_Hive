<template>
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <section class="min-vh-100 position-relative background-radial-gradient overflow-hidden">
        <div class="position-absolute top-0 start-0 mt-6 text-white fw-bold text-cenetr">
            <RouterLink :to="{ name: 'SignIn' }" class="text-sm ml-2 mr-2 hover:text-blue-500 cursor-pointer">
                <img style="width: 200px" :src="scorehive" alt="Image" />
            </RouterLink>

        </div>
        <div class="d-flex align-items-center">
            <div class="container px-4 py-5 px-md-5 text-center text-lg-start my-5">
                <div class="row gx-lg-5 align-items-center mb-5">
                    <div class="col-lg-6 mb-5 mb-lg-0" style="z-index: 10">
                        <h1 class="my-5 display-5 fw-bold ls-tight" style="color: hsl(218, 81%, 95%)">
                            The best way <br />
                            <span style="color: hsl(218, 81%, 75%)">to manage your games</span>
                        </h1>
                        <p class="mb-4 opacity-70" style="color: hsl(218, 81%, 85%)">
                            A complete solution to manage your cricket tournaments and matches
                        </p>
                    </div>

                    <div class="col-lg-6 mb-5 mb-lg-0 position-relative">
                        <GlassCard>
                            <div class="card-body px-4 px-md-5">
                                <form>
                                    <div class="row">
                                        <div class="col-md-12 mb-4">
                                            <h4>Reset Password..?</h4>
                                        </div>
                                    </div>
                                    <!-- Email input -->
                                    <div class="form-floating">
                                        <input type="email" class="form-control" id="floatingEmail"
                                            placeholder="name@example.com" v-model="email" />
                                        <label class="form-label text-muted" for="floatingEmail">Email address</label>
                                    </div>
                                    <div v-for="(error, index) in v$.email.$errors" :key="index" class="error">
  <span v-if="error.$params.type == 'required'"><small>Please enter your email</small></span>
  <span v-if="error.$params.type == 'email'"><small>Please enter a valid email</small></span>
</div>

                                    <div v-if="v$.email.$errors.length == 0" class="mb-3"></div>
                                    <cbutton class="mb-4 py-3" fullWidth variant="gradient" color="primary"
                                        :disabled="isLoading" @click.prevent="submit()"><span v-if="isLoading"
                                            class="spinner-border spinner-border-sm me-2" role="status"
                                            aria-hidden="true"></span>
                                        <span v-else class="fw-bold">Submit</span></cbutton>
                                </form>
                            </div>
                        </GlassCard>

                    </div>
                </div>
            </div>
        </div>
        <P class="position-absolute bottom-0 start-50 translate-middle-x fs-7 text-white"> © 2023 ScoreHive </P>
    </section>
</template>  
<script>
import cric from "@/assets/img/cric.png";
import scorehive from "@/assets/img/logo_6.png";
import errorCodes from "@/services/errorCodes.json"
import { sendForgotEmail } from "@/services/authService";
import { useVuelidate } from "@vuelidate/core";
import Swal from 'sweetalert2';
import {
    required,
    email,
    maxLength,
} from "@vuelidate/validators";
import cbutton from "@/components/Button.vue";
import GlassCard from "@/components/GlassCard.vue";
export default {
    name: "sende-mail",
    components: {
        cbutton,
        GlassCard
    },
    setup() {
        return { v$: useVuelidate() };
      
    },
    data() {
        return {
            email: "",
            isLoading: false,
            cric: cric,
            scorehive: scorehive,
        };
    },
    validations() {
        return {
            email: {
                required,
                email,
                maxLength: maxLength(100),
            },
        };
    },
    methods: {
        handleError(error) {
            let errorMessage = '';
            // Determine the error message based on the error code
            if (error.response && error.response.status === 400) {
                errorMessage = 'No user account found associated with the given mail';
            } else {
                errorMessage = 'An unknown error occurred.';
            }
            //Show the error message using swal
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: errorMessage,
            });
        },
        async submit() {
            const isValid = await this.v$.$validate();

            if (isValid) {
                this.isLoading = true;
                sendForgotEmail(this.$data).then(
                    () => {
                        Swal.fire('Thank you...', 'Please Check Your Mail')
                        this.$data.email = ''
                        this.$router.push("sign-in");
                    },
                    (error) => {
                        this.isLoading = false;
                        const errorMessage = errorCodes[error.response.data.error_code] || "Oops.. Some unknown error occurred..!"
                        Swal.fire({
                            icon: "error",
                            title: "Failed",
                            text: errorMessage,
                        });
                        this.$data.email = ''
                        this.isLoading = false;
                    }
                );
            }
            else {
                this.isLoading = false;
            }
        },
    },
};
</script>
    