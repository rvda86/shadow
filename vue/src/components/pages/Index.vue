<template>

    <div id="index"> 

        <div class="index-story wrap">
            <div class="benefits">
                
                <h3>Start a journal</h3>

                <p>
                    Journaling reduces your stress levels, writing is a cathartic experience. 
                    By expressing yourself you can better manage your emotions.
                </p>

                <p>
                    And journaling helps you gain insight into your mind by 
                    increasing your awareness of what's going on inside your mind.
                </p>

            </div>

            <div>
                <img class="benefits-img" src="../../assets/images/kenny-eliason-HXjtPt_XRAQ-unsplash.jpg">
                <p class="attribute-link">Photo by 
                    <a href="https://unsplash.com/@neonbrand?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Kenny Eliason</a> on 
                    <a href="https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
                </p>
            </div>

        </div>


        <div class="index-story wrap-reverse">

            <div>
                <img class="benefits-img" src="../../assets/images/eden-constantino-bTukYI4DjOs-unsplash.jpg" />
                <p class="attribute-link">Photo by 
                    <a href="https://unsplash.com/@edenconstantin0?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Eden Constantino</a> on 
                    <a href="https://unsplash.com/s/photos/todo?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
                </p>
            </div>

            <div class="benefits">

                <h3>Create ToDo lists</h3>

                <p>Feel less overwhelmed by breaking down tasks into smaller, more manageable, chunks.</p>
                <p>Increase your productivity by clarifying and prioritizing your tasks.</p>
                <p>Feel good when you tick off a task on your list and get more motivated.</p>
            
            </div>

        </div>
       
        <div class="index-story wrap">

            <div class="benefits">

                <h3>Track your habits</h3>

                <p>Increase your motivation. It takes time to build a new habit, with a habit tracker you make your progress visible.</p>
                <p>Become more aware of your behavior by being able to see how you did every day</p>
                <p>Be more likely to succeed at changing your behavior</p>

            </div>

            <div>
                <img class="benefits-img" src="../../assets/images/drew-beamer-uejtDqpJ7ig-unsplash.jpg" />
                <p class="attribute-link">
                    Photo by <a href="https://unsplash.com/@drew_beamer?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Drew Beamer</a> on 
                    <a href="https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
                </p>
            </div>

        </div>

        <h4>Get started</h4>

        <router-link :to="{name: 'createAccount'}"><button class="button">Create Account</button></router-link>

    </div>

</template>

<script>

import { mapActions } from 'vuex'

export default {
    name: 'Index',
    data() {
        return {
            username: "",
            password: ""
        }
    },
    methods: {
        ...mapActions(["getTokenRequest"]),
        submitHandler() {
            this.getTokenRequest({username: this.username, password: this.password})
        }

    }
}
</script>

<style>

#index {
    text-align: center;
    font-family: sans-serif;
}

.index-story {
    display: flex;
    justify-content: center;
    margin: 10px;
}

.benefits {
    width: 500px;
    padding: 10px;
    margin: 5px 5px;
    background-color: white;
    border-radius: 5%;
}

.benefits-img {
    width: 300px;
    border-radius: 5%;
    margin: 5px 5px;
}

.attribute-link {
    font-size: 0.5em;
}

.wrap {
    flex-wrap: wrap;
}

.wrap-reverse {
    flex-wrap: wrap-reverse;
}

@media screen and (max-width: 800px) {
        .benefits {
        width: 300px;
    }

    .benefits-img {
        width: 300px;
    }
}


</style>