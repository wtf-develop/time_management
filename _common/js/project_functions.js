function isGoodResponse(json) {
    if (json.error !== undefined && json.error.state !== undefined && json.error.state) {
        alert(json.error.title + "\n" + json.error.message); // replace to your own implementation
        return false;
    }
    return true;
}
