import Vue from 'vue'
import Vuex from 'vuex'
import actions from './actions'
import mutations from './mutations'
// import middlewares from './middlewares'

Vue.use(Vuex)

const state = {
  available_card_numbers: [], // 导入的允许充值的油卡
  loading: false,
  card_detail: {}, // 显示待编辑的详情
  selected_card: {}, // 充值时候选中的油卡
  pay_infos: [],
  cards: []
}

const store = new Vuex.Store(
  {
    state,
    actions,
    // middlewares,
    mutations
  }
)
if (module.hot) {
  // 使 actions 和 mutations 成为可热重载模块
  module.hot.accept(
    ['./actions', './mutations'], () => {
      // 获取更新后的模块
      // 因为 babel 6 的模块编译格式问题，这里需要加上 .default
      const newActions = require('./actions').default
      const newMutations = require('./mutations').default
      // 加载新模块
      store.hotUpdate(
        {
          actions: newActions,
          mutations: newMutations
        }
      )
    }
  )
}
export default store
