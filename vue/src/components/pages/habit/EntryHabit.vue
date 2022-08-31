<template>
    <div>

        <div class="card" v-show="!editing">
            <div class="flex-row habit-entry">
                <p class="margin-right-auto"><strong>{{ entry.name }}</strong></p>
                <font-awesome-icon class="margin-right-10" icon="fa-solid fa-pen" @click="toggleEditing"/>
                <font-awesome-icon icon="fa-solid fa-trash" @click="deleteHandler" />
            </div>
            <p class="small-font">{{ entry.days[index-6].date }} to {{ entry.days[index].date }}</p>

            <table>
                <tr>
                    <td class="habit-column" @click="showPreviousWeek()"><font-awesome-icon icon="fa-solid fa-angle-left" /></td>
                    <td class="habit-column">M</td>
                    <td class="habit-column">T</td>
                    <td class="habit-column">W</td>
                    <td class="habit-column">T</td>
                    <td class="habit-column">F</td>
                    <td class="habit-column">S</td>
                    <td class="habit-column">S</td>
                    <td class="habit-column" @click="showNextWeek()"><font-awesome-icon icon="fa-solid fa-angle-right" /></td>
                </tr>
                <tr>
                    <td class="habit-column"></td>
                    <td class="habit-column" @click="updateDay(entry.days[index-6])">
                        <font-awesome-icon v-show="(entry.days[index-6].completed === 0)" icon='fa-solid fa-xmark' />
                        <font-awesome-icon v-show="(entry.days[index-6].completed === 1)" icon='fa-solid fa-check' />
                    </td>
                    <td class="habit-column" @click="updateDay(entry.days[index-5])">
                        <font-awesome-icon v-show="(entry.days[index-5].completed === 0)" icon='fa-solid fa-xmark' />
                        <font-awesome-icon v-show="(entry.days[index-5].completed === 1)" icon='fa-solid fa-check' />
                    </td>
                    <td class="habit-column" @click="updateDay(entry.days[index-4])">
                        <font-awesome-icon v-show="(entry.days[index-4].completed === 0)" icon='fa-solid fa-xmark' />
                        <font-awesome-icon v-show="(entry.days[index-4].completed === 1)" icon='fa-solid fa-check' />
                    </td>
                    <td class="habit-column" @click="updateDay(entry.days[index-3])">
                        <font-awesome-icon v-show="(entry.days[index-3].completed === 0)" icon='fa-solid fa-xmark' />
                        <font-awesome-icon v-show="(entry.days[index-3].completed === 1)" icon='fa-solid fa-check' />
                    </td>
                    <td class="habit-column" @click="updateDay(entry.days[index-2])">
                        <font-awesome-icon v-show="(entry.days[index-2].completed === 0)" icon='fa-solid fa-xmark' />
                        <font-awesome-icon v-show="(entry.days[index-2].completed === 1)" icon='fa-solid fa-check' />
                    </td>
                    <td class="habit-column" @click="updateDay(entry.days[index-1])">
                        <font-awesome-icon v-show="(entry.days[index-1].completed === 0)" icon='fa-solid fa-xmark' />
                        <font-awesome-icon v-show="(entry.days[index-1].completed === 1)" icon='fa-solid fa-check' />
                    </td>
                    <td class="habit-column" @click="updateDay(entry.days[index])">
                        <font-awesome-icon v-show="(entry.days[index].completed === 0)" icon='fa-solid fa-xmark' />
                        <font-awesome-icon v-show="(entry.days[index].completed === 1)" icon='fa-solid fa-check' />
                    </td>
                    <td class="habit-column"></td>
                </tr>
            </table>

        </div>

        <div class="card" v-show="editing">
            <div class="flex-row todo-entry">
                <input class="input margin-right-auto" type="text" placeholder="habit name" v-model="name" required>
                <button class="button background-red" @click="toggleEditing">Cancel</button>
                <button class="button" @click="updateHandler">Save</button>
            </div>
        </div>

    </div>
</template>

<script>

import { mapMutations, mapActions } from 'vuex'

export default {
    name: 'EntryHabit',
    data() {
        return {
            editing: false,
            name: this.entry.name,
            index: this.entry.days.length - 1,
        }
    },
    props: {
        entry: Object
    },
    methods: {
        ...mapActions(["sendEntryDataRequest"]),
        ...mapMutations(["toggleModal", "setModalPayload"]),
        toggleEditing() {
            this.editing = !this.editing
        },
        updateHandler() {
            this.sendEntryDataRequest(['PUT', {type: 'habit', name: this.name, days: this.entry.days, id: this.entry.id}])
            this.editing = false
        },
        deleteHandler() {
            this.setModalPayload({func: this.sendEntryDataRequest, payload: ['DELETE', {type: 'habit', id: this.entry.id}]})
            this.toggleModal()
        },
        updateDay(day) {
            day.completed = (day.completed == 0) ? 1 : 0
            this.sendEntryDataRequest(['PUT', {type: 'habit', name: this.entry.name, days: this.entry.days, id: this.entry.id}])
        },
        showPreviousWeek() {
            if (this.index > 6) {
                this.index -= 7
            } else {
                this.index = this.entry.days.length - 1
            }
        },
        showNextWeek() {
            if (this.index === this.entry.days.length - 1) {
                this.index = 6
            } else {
                this.index += 7
            }
        }
    },
}


</script>