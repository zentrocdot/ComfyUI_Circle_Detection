import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

app.registerExtension({
	name: "zentrocdot.data_updater",

	async setup() {
		api.addEventListener("zentrocdot.data_updater.node_processed", function (event) {
			const nodeId = parseInt(event.detail.node);
			const widgetName = event.detail.widget;
			const text = event.detail.text;
			const node = app.graph.nodes.find(n => n.id === nodeId);
			if (!node) {
				console.error(`Node to update (#${nodeId}) not found.`);
				return;
			}
			const widget = node.widgets.find(w => w.name === widgetName);
			if (!widget) {
				console.error(`Widget to update (#${nodeId}:${widgetName}) not found.`);
				return;
			}
			widget.value = text;
		});
	},
});
