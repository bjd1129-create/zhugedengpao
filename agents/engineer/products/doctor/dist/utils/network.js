"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.checkGatewayAPI = checkGatewayAPI;
exports.checkNetworkConnectivity = checkNetworkConnectivity;
const node_fetch_1 = __importDefault(require("node-fetch"));
/**
 * 检测 Gateway API 端点是否可达
 */
async function checkGatewayAPI(url = 'http://localhost:18789/health') {
    try {
        const response = await (0, node_fetch_1.default)(url, {
            method: 'GET',
            timeout: 5000
        });
        if (response.ok) {
            return {
                name: 'Gateway API',
                status: 'pass',
                message: `API 端点响应正常 (${response.status})`
            };
        }
        return {
            name: 'Gateway API',
            status: 'fail',
            message: `API 返回错误状态码 ${response.status}`,
            details: `URL: ${url}`
        };
    }
    catch (error) {
        return {
            name: 'Gateway API',
            status: 'fail',
            message: `无法连接到 API 端点`,
            details: error instanceof Error ? error.message : String(error)
        };
    }
}
/**
 * 检测网络连通性
 */
async function checkNetworkConnectivity() {
    const results = [];
    // 检测 localhost
    try {
        const response = await (0, node_fetch_1.default)('http://localhost:18789/health', {
            method: 'GET',
            timeout: 3000
        });
        results.push({
            name: 'Localhost',
            status: 'pass',
            message: '本地连接正常'
        });
    }
    catch {
        results.push({
            name: 'Localhost',
            status: 'warn',
            message: '本地连接不可达（Gateway 可能未运行）'
        });
    }
    return results;
}
