import VueChartkick from 'vue-chartkick'
import Chart from 'chart.js/auto/auto.js'
import 'chartjs-adapter-date-fns'

import type { UserModule } from '~/types'

export const install: UserModule = ({ app }) => {
  app.use(VueChartkick.use(Chart))
}
